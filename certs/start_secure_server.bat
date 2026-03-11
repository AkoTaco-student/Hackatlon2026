@echo off

echo Starting Mosquitto...
start cmd /k "C:\Program Files\mosquitto\mosquitto.exe -c C:\Users\Akos\mosquitto\mosquitto-secure.conf -v"

timeout /t 2 > nul

echo Starting Python Receiver...
start cmd /k "python C:\Users\Akos\Downloads\akos_certs\certs\receive_file.py"
