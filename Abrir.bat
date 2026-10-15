@echo off
rem Abre el panel sin Claude: doble clic. Cerrar esta ventana lo apaga.
cd /d "%~dp0"
title No Noise News - si cierras esta ventana, se apaga
set PY=python
where py >nul 2>nul && set PY=py
%PY% panel.py --abrir
if errorlevel 1 pause
