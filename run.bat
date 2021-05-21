echo off
mode con: cols=100 lines=40
cls
python ./main.py %1 10
pause