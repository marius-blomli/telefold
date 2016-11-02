@echo off

IF %1.==. GOTO NoDebug
IF "%1"=="DEBUG" GOTO Debug
GOTO UnknownCommand

:NoDebug

@echo Running "kernel_density.py" in arcgis context
c:\Python27\ArcGIS10.4\python.exe kernel_density.py

GOTO End

:Debug

@echo PDB-debugging "kernel_density.py" in arcgis context
c:\Python27\ArcGIS10.4\python.exe -m pdb kernel_density.py

GOTO End

:UnknownCommand

@echo Unknown command %1
GOTO End

:End

@echo Exiting