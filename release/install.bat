@ echo off
set base_dir=C:\
set py_dir=%base_dir%Python33
set hb_dir=%base_dir%hb_service
set ig_dir=%base_dir%imgInfoGeter
set py_lib=%py_dir%\Lib\site-packages

if %PROCESSOR_ARCHITECTURE% == AMD64 goto setup64
if %PROCESSOR_ARCHITECTURE% == x86 goto setup32

:setup64
:: setup python
msiexec /qb! /i python-3.3.1.amd64.msi TARGETDIR=%py_dir% ALLUSERS=1 ADDLOCAL=ALL
:: set python path
:: reg add "HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d "%py_dir%;%Path%" /f
:: wmic ENVIRONMENT where "name='path' and username='<system>'" set VariableValue="%py_dir%;%path%"

:: setup pyodbc
copy /b lib.win-amd64-3.3\pyodbc.pyd %py_lib%

:: setup hb_service
md %hb_dir%
copy hb_service\* %hb_dir%

:: setup imgInfoGeter
md %ig_dir%
copy imgInfoGeter\* %ig_dir%

goto exit

:setup32
:: setup python
msiexec /qb! /i python-3.3.1.msi TARGETDIR=%py_dir% ALLUSERS=1 ADDLOCAL=ALL

:: setup pyodbc
copy /b lib.win32-3.3\pyodbc.pyd %py_lib%

:: setup hb_service
md %hb_dir%
copy hb_service\* %hb_dir%

:: setup imgInfoGeter
md %ig_dir%
copy imgInfoGeter\* %ig_dir%

goto exit

:exit
echo install exit!
pause

