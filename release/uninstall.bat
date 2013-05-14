@echo off
set base_dir=C:\
set py_dir=%base_dir%Python33
set hb_dir=%base_dir%hb_service
set ig_dir=%base_dir%imgInfoGeter
set py_lib=%py_dir%\Lib\site-packages

if %PROCESSOR_ARCHITECTURE% == AMD64 goto uninstall64
if %PROCESSOR_ARCHITECTURE% == x86 goto uninstall32

:uninstall64
:: uninstall pyodbc
del %py_lib%\pyodbc.pyd

:: unintall python
msiexec /qb! /x python-3.3.1.amd64.msi

:: uninstall hb_service
rd /s /q %hb_dir%

:: uninstall imgInfoGeter
rd /s /q %ig_dir%

goto exit

:uninstall32
:: uninstall pyodbc
del %py_lib%\pyodbc.pyd

:: unintall python
msiexec /l* ^&1 /qb! /x python-3.3.1.msi

:: uninstall hb_service
rd /s /q %hb_dir%

:: uninstall imgInfoGeter
rd /s /q %ig_dir%

goto exit

:exit
echo uninstall exit!
pause