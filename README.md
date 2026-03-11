# Hackatlon2026
# Made by Akos Nagy

# This code simply put: Made by Akos Nagy 

# You launch a secure mosquitto server using elliptic krypto cybersecurity keys, the newest and best keys as of March 2026. On one end of the secure server, a Ai model of your choice (I used open source ollama3) can receive and respond to your inputs. The frontend is very simple because the main focus of this program is the cybersecurity part.

# Running the program

# You need to configure your IP adress to be correct in files mosquitto.conf, x509.ext and possibly add it to system32 if you run on a simple computer. This way, everything works over your own secure network (LAN -network)

# Code for starting the server: (After activating virtual enviroment) - btw you will most likely have to make changes since your files will have different names

# (venv) PS C:\Hackatlon2026> & "C:\Program Files\mosquitto\mosquitto.exe" -c C:\Hackatlon2026\mosquitto.conf -v

# (venv) PS C:\Hackatlon2026> ollama run llama3      

# (venv) PS C:\Hackatlon2026> python ai.py           

# -- Now, on the receiving computer

# (venv) PS C:\Hackatlon2026> python interface/app.py

# Make sure both host and receiver have their appropriate elliptic krypto keys (.pem files under /certs)

# By the way, the interface avatar doesn't work yet.



To use the code: 


download openssl
download mosquitto
download python

