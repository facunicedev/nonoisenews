---
name: actualizar
description: Trae la última versión de No Noise News desde GitHub sin tocar sus datos (perfil, noticias, historial). Úsala al empezar si toca (una vez por semana, lo decide el propio comando) o cuando ella pida actualizar.
---

1. Ejecuta `py panel.py --actualizar` (añade `--si-toca` si no lo ha pedido ella: así solo actúa una vez por semana).
2. Según lo que responda:
   - `no toca` o `ya estaba al día`: no digas nada (si lo pidió ella: «Ya estaba al día»).
   - `actualizado: …`: dile en una frase que hay versión nueva. Si en la lista sale `panel.py`, reinicia el panel. Si sale `CLAUDE.md` o algo de `.claude/`, vuelve a leer `CLAUDE.md`: tus instrucciones han cambiado.
   - `error: …`: no fuerces nada ni borres nada. Dile en una frase que no se pudo actualizar y sigue con normalidad. Si el error habla de cambios locales, pregúntale antes de tocarlos.
3. `datos/` nunca se toca: ahí está todo lo suyo.
