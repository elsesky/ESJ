@ECHO OFF
DEL /F /Q esj.exe
DEL /F /Q esj_ui.exe
python setup_esj.py py2exe 2>NUL
python setup_esj_ui.py py2exe 2>NUL
PUSHD dist 1>NUL
DEL /F /Q w9xpopen.exe
REM MOVE /Y *.exe ../
copy esj.exe ..
copy esj_ui.exe ..
POPD
REM RD /S /Q dist
RD /S /Q build
DEL /F /Q *.PYC
DEL /F /Q *.LOG
PUSHD ui
DEL /F /Q *.PYC
POPD
REM signtool sign /f elsesky.pfx /p dengbo  /t http://timestamp.verisign.com/scripts/timstamp.dll /v DMZJ_MH_NEW.exe