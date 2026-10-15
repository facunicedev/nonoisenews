"""No Noise News, el panel local: sirve web/ y apunta cada botón en datos/acciones.log para que Claude lo vea.

    py panel.py            sirve en http://127.0.0.1:8766
    py panel.py --abrir    y abre el navegador
    py panel.py --selftest
    py panel.py --actualizar [--si-toca]   trae la última versión de GitHub sin tocar datos/

Lo que escribe el panel: datos/perfil.json (cuestionario, «Tu búsqueda» y el porqué de cada botón) y
datos/acciones.log (una línea por botón). datos/noticias.json solo lo escribe Claude.
"""
import json
import secrets
import sys
import tempfile
import threading
import io
import subprocess
import urllib.request
import webbrowser
import zipfile
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
WEB = RAIZ / "web"
PUERTO = 8766  # OfferLens usa 8765
REPO = "facunicedev/nonoisenews"  # ponytail: si el repo cambia de nombre, solo aquí
MAX_CUERPO = 200_000
TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".svg": "image/svg+xml", ".png": "image/png"}


def leer(f, defecto):
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return defecto


def escribir(f, dato):
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(dato, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(f)


def accion(datos, a):
    """Un botón de la página. Lo que cambia el perfil queda guardado; todo queda en el log para Claude."""
    tipo, perfil_f = a.get("tipo"), datos / "perfil.json"
    if tipo == "guardar_perfil":
        nuevo = a.get("perfil")
        if not isinstance(nuevo, dict):
            raise ValueError("Falta el perfil.")
        antes = leer(perfil_f, None)
        nuevo["feedback"] = (antes or {}).get("feedback", [])  # el porqué de cada botón no se pierde al reajustar
        escribir(perfil_f, nuevo)
        detalle = {"primera_vez": antes is None, "antes": {k: v for k, v in (antes or {}).items() if k != "feedback"},
                   "ahora": {k: v for k, v in nuevo.items() if k != "feedback"}}
    elif tipo in ("mas", "no_interesa", "pregunta"):
        if not a.get("id"):
            raise ValueError("Falta la noticia.")
        if tipo == "pregunta" and not str(a.get("pregunta") or "").strip():
            raise ValueError("Falta la pregunta.")
        n = next((n for n in leer(datos / "noticias.json", {}).get("noticias", []) if n.get("id") == a["id"]), {})
        detalle = {"id": a["id"], "tema": n.get("tema"), "titular": n.get("titular"),
                   "porque": str(a.get("porque") or "").strip()[:1000]}
        if tipo == "pregunta":  # lo que pregunta también dice qué le interesa
            detalle = {k: v for k, v in detalle.items() if k != "porque"} | {"pregunta": str(a["pregunta"]).strip()[:2000]}
        perfil = leer(perfil_f, {})
        perfil.setdefault("feedback", []).append(dict(detalle, tipo=tipo, fecha=datetime.now().date().isoformat()))
        escribir(perfil_f, perfil)
    elif tipo == "idioma":  # cambió el idioma en la página: el perfil se queda con él y Claude traduce
        idioma = str(a.get("idioma") or "").strip()[:10]
        perfil = leer(perfil_f, None)
        if not idioma or perfil is None:
            raise ValueError("Falta el idioma.")
        detalle = {"antes": perfil.get("idioma"), "ahora": idioma}
        escribir(perfil_f, perfil | {"idioma": idioma})
    elif tipo == "informame":
        detalle = {"idioma": str(a.get("idioma") or "")}
    else:
        raise ValueError("No sé hacer eso.")
    with (datos / "acciones.log").open("a", encoding="utf-8") as h:
        h.write(f"{datetime.now().isoformat(timespec='seconds')}\t{tipo}\t{json.dumps(detalle, ensure_ascii=False)}\n")


def version(datos):
    """Cambia cuando cambia algo en datos/: la página recarga sola."""
    return str(hash(tuple((p.name, s.st_mtime_ns, s.st_size) for p in sorted(datos.glob("*.json")) if (s := p.stat()))))


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def responder(self, codigo, cuerpo, tipo="application/json; charset=utf-8"):
        if not isinstance(cuerpo, bytes):
            cuerpo = json.dumps(cuerpo, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def local(self):
        puerto = self.server.server_address[1]
        return self.headers.get("Host") in {f"{h}:{puerto}" for h in ("127.0.0.1", "localhost", "[::1]")}

    def do_POST(self):
        largo = int(self.headers.get("Content-Length") or 0)
        if not self.local() or self.path != "/api/accion" or largo > MAX_CUERPO or \
                not secrets.compare_digest(self.headers.get("X-Token", ""), self.server.token):
            return self.responder(403, {"error": "solo desde la página"})
        try:
            a = json.loads(self.rfile.read(largo))
            accion(self.server.datos, a if isinstance(a, dict) else {})
        except ValueError as err:
            return self.responder(400, {"error": str(err)})
        self.responder(200, {"ok": True})

    def do_GET(self):
        if not self.local():
            return self.responder(403, {"error": "solo desde este ordenador"})
        ruta, datos = self.path.split("?")[0], self.server.datos
        if ruta == "/api/version":
            return self.responder(200, {"version": version(datos)})
        if ruta == "/api/estado":
            return self.responder(200, {"perfil": leer(datos / "perfil.json", None),
                                        "noticias": leer(datos / "noticias.json", None),
                                        "general": leer(datos / "general.json", None), "token": self.server.token})
        f = (WEB / (ruta.lstrip("/") or "index.html")).resolve()
        if WEB not in f.parents or not f.is_file() or f.suffix not in TIPOS:
            return self.responder(404, {"error": "no existe"})
        self.responder(200, f.read_bytes(), TIPOS[f.suffix])


def servidor(datos, puerto):
    datos.mkdir(exist_ok=True)
    s = ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    s.datos, s.token = datos, secrets.token_urlsafe(24)
    return s


def actualizar(raiz=RAIZ, si_toca=False, zip_bytes=None):
    """Trae la última versión: git pull si es un clon; si vino en ZIP, lo descarga y pisa todo menos datos/."""
    marca = raiz / "datos" / ".actualizado"
    if si_toca and marca.is_file() and (date.today() - date.fromisoformat(marca.read_text().strip())).days < 7:
        return "no toca"
    if zip_bytes is None and (raiz / ".git").exists():
        git = lambda *a: subprocess.run(["git", *a], cwd=raiz, capture_output=True, text=True)
        antes, r = git("rev-parse", "HEAD").stdout, git("pull", "--ff-only")
        if r.returncode:  # p. ej. alguien tocó un archivo del programa: no se fuerza nada
            return "error: " + (r.stderr or r.stdout).strip()
        cambiado = git("diff", "--name-only", antes.strip(), "HEAD").stdout.split() if antes != git("rev-parse", "HEAD").stdout else []
    else:
        if zip_bytes is None:
            url = f"https://codeload.github.com/{REPO}/zip/refs/heads/main"
            with urllib.request.urlopen(url, timeout=60) as h:
                zip_bytes = h.read()
        cambiado = []
        # ponytail: no borra archivos que desaparezcan del repo; añadirlo si algún día estorban
        for m in zipfile.ZipFile(io.BytesIO(zip_bytes)).infolist():
            rel = Path(*Path(m.filename).parts[1:])  # quita la carpeta «repo-main/»
            destino = (raiz / rel).resolve()
            if m.is_dir() or not rel.parts or rel.parts[0] == "datos" or raiz.resolve() not in destino.parents:
                continue
            nuevo = zipfile.ZipFile(io.BytesIO(zip_bytes)).read(m)
            if not destino.is_file() or destino.read_bytes() != nuevo:
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_bytes(nuevo)
                cambiado.append(str(rel))
    marca.parent.mkdir(exist_ok=True)
    marca.write_text(date.today().isoformat())
    return f"actualizado: {', '.join(cambiado)}" if cambiado else "ya estaba al día"


def selftest():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        s = servidor(d, 0)
        threading.Thread(target=s.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{s.server_address[1]}"

        def pedir(ruta, cuerpo=None, **h):
            datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
            try:
                with urllib.request.urlopen(urllib.request.Request(base + ruta, datos, headers=h)) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                return e.code, e.read()

        st, cuerpo = pedir("/api/estado")
        e = json.loads(cuerpo)
        assert st == 200 and e["perfil"] is None and e["noticias"] is None and e["general"] is None
        tok = {"X-Token": e["token"], "Content-Type": "application/json"}
        assert pedir("/api/accion", {"tipo": "informame"})[0] == 403, "sin token no"
        assert pedir("/api/estado", Host="malo.com")[0] == 403
        assert pedir("/../panel.py")[0] == 404
        v = json.loads(pedir("/api/version")[1])["version"]
        perfil = {"cuantas": 10, "temas": [{"tema": "Economía", "peso": "mas"}], "prosa": "sin política"}
        assert pedir("/api/accion", {"tipo": "guardar_perfil", "perfil": perfil}, **tok)[0] == 200
        assert json.loads(pedir("/api/version")[1])["version"] != v, "guardar cambia la versión"
        escribir(d / "noticias.json", {"noticias": [{"id": "n1", "tema": "Economía", "titular": "T"}]})
        assert pedir("/api/accion", {"tipo": "no_interesa", "id": "n1", "porque": "ya lo sé"}, **tok)[0] == 200
        assert pedir("/api/accion", {"tipo": "guardar_perfil", "perfil": dict(perfil, cuantas=5)}, **tok)[0] == 200
        p = leer(d / "perfil.json", {})
        assert p["cuantas"] == 5 and p["feedback"][0]["porque"] == "ya lo sé", "el porqué sobrevive al reajuste"
        assert pedir("/api/accion", {"tipo": "pregunta", "id": "n1", "pregunta": " "}, **tok)[0] == 400
        assert pedir("/api/accion", {"tipo": "pregunta", "id": "n1", "pregunta": "¿Qué es el BCE?"}, **tok)[0] == 200
        assert pedir("/api/accion", {"tipo": "borrar_todo"}, **tok)[0] == 400
        assert pedir("/api/accion", {"tipo": "idioma", "idioma": "en"}, **tok)[0] == 200
        p = leer(d / "perfil.json", {})
        assert p["idioma"] == "en" and len(p["feedback"]) == 2, "cambiar idioma no pierde el feedback"
        log = (d / "acciones.log").read_text(encoding="utf-8")
        assert "\tno_interesa\t" in log and '"titular": "T"' in log and log.count("\n") == 5 and '"pregunta": "¿Qué es el BCE?"' in log
        assert b"<html" in pedir("/")[1]
        s.shutdown()
        s.server_close()
    with tempfile.TemporaryDirectory() as t:  # actualizar desde un ZIP no toca datos/ ni sale de la carpeta
        d = Path(t)
        (d / "datos").mkdir()
        (d / "datos" / "perfil.json").write_text("mío")
        z = io.BytesIO()
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("repo-main/panel.py", "nuevo")
            zf.writestr("repo-main/datos/perfil.json", "pisado")
            zf.writestr("repo-main/../fuera.txt", "x")
        assert actualizar(d, zip_bytes=z.getvalue()) == "actualizado: panel.py"
        assert (d / "datos" / "perfil.json").read_text() == "mío" and not (d.parent / "fuera.txt").exists()
        assert actualizar(d, si_toca=True) == "no toca"
        assert actualizar(d, zip_bytes=z.getvalue()) == "ya estaba al día"
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit()
    if "--actualizar" in sys.argv:
        print(actualizar(si_toca="--si-toca" in sys.argv))
        sys.exit()
    s = servidor(RAIZ / "datos", PUERTO)
    url = f"http://127.0.0.1:{PUERTO}"
    print(f"Abierto en {url}  (cierra esta ventana para apagarlo)")
    if "--abrir" in sys.argv:
        webbrowser.open(url)
    s.serve_forever()
