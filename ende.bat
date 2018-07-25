
@echo off
set de_folder=%~dp0\priv
set en_folder=%~dp0\priv_en
echo de_folder=%de_folder%
echo en_folder=%de_folder%

set /p cho=en(0) or de(1):
:: echo cho=%cho%
if "%cho%" == "0" (
C:/ProgramData/Anaconda3/python do_crypto.py en %de_folder% %en_folder%
echo ---en done.
) else if "%cho%" == "1" (
:: delete the contents of de_folder
For /d /r "%de_folder%\" %%i in (*) do (Rd /q /s "%%i" 2>nul)
Del /q /a "%de_folder%\*.*"
C:/ProgramData/Anaconda3/python do_crypto.py de %de_folder% %en_folder%
echo ---de done.
) else (
echo Error: not select
)

pause