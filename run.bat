echo off
mode con: cols=100 lines=40
cls

if [%1]==[] goto usage

python .\main.py %1 10
goto end

:usage:
echo You must specify a file.
pause
:end:
