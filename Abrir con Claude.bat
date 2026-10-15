@echo off
rem Abre esta carpeta en la app de Claude (pestaña Code) con un saludo escrito: solo hay que pulsar Intro.
rem Opens this folder in the Claude app (Code tab) with a greeting typed in: just press Enter.
cd /d "%~dp0"
powershell -NoProfile -Command "$hola = if ((Get-Culture).TwoLetterISOLanguageName -eq 'es') { 'Hola' } else { 'Hi' }; Start-Process ('claude://code/new?folder=' + [uri]::EscapeDataString((Get-Location).Path) + '&q=' + [uri]::EscapeDataString($hola))"
