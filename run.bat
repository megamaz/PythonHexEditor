echo off
mode con: cols=100 lines=40
cls


if not exist venv (
    echo Setting up...
    call py -m venv venv
    call .\venv\Scripts\activate
    call py -m pip install -r .\requirements.txt
    call deactivate

    cls
    echo Setup finished.
)

if [%1]==[] goto usage

call .\venv\Scripts\activate
call py .\main.py %1 10
goto end

:usage:
echo You must specify a file.
pause
:end:
