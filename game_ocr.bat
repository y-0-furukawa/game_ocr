@echo off
pushd %~dp0

:ç≈è¨âªèÛë‘Ç≈é¿çsÇ∑ÇÈ
if not "%X_MIMIMIZED%"=="1" (
    set X_MIMIMIZED=1
    start /min cmd /c,"%~0" %*
    exit
)

.venv\Scripts\python.exe main.py

popd

:pause
