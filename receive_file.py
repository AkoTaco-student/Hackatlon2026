import paho.mqtt.client as mqtt
import ssl
import base64
import sys
import os

# Default broker name — can be a LAN hostname or IP. Use env `BROKER_HOST` or
# pass as first CLI argument to override.
BROKER = os.environ.get("BROKER_HOST") or (sys.argv[1] if len(sys.argv) > 1 else "HackatlonServer")

BROKER_HOST = "172.20.10.6"
#client.tls_insecure_set(False)

PORT = 8883


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")



#TOPIC = "secure/files"
TOPIC = "secure/files/response"


def on_message(client, userdata, msg):
    print("[RECEIVER] File received!")

    filename, encoded = msg.payload.decode().split("::")

    file_data = base64.b64decode(encoded)

    with open("responce_" + filename, "wb") as f:
        f.write(file_data)

    print(f"[RECEIVER] Saved as responce_{filename}")


client = mqtt.Client()
client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

# For quick LAN testing where the server cert's hostname/IP doesn't match the
# broker you connect to, set environment `TLS_INSECURE=1` to disable hostname
# verification (not recommended for production).
if os.environ.get("TLS_INSECURE") in ("1", "true", "True"):
    client.tls_insecure_set(True)

client.on_message = on_message

# Resolve and report the broker address before connecting, to help LAN usage.
try:
    resolved = None
    try:
        resolved = __import__("socket").getaddrinfo(BROKER, PORT)
    except Exception:
        resolved = None
    if resolved:
        addr = resolved[0][4][0]
        print(f"[RECEIVER] Resolving broker {BROKER} -> {addr}")
    else:
        print(f"[RECEIVER] Broker name {BROKER} did not resolve locally; trying as given")

    client.connect(BROKER, PORT)
except Exception as e:
    print(f"[RECEIVER] Could not connect to broker {BROKER}:{PORT} - {e}")
    sys.exit(1)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[RECEIVER] Connected successfully")
        client.subscribe(TOPIC)
    else:
        print("[RECEIVER] Connection failed:", rc)

client.on_connect = on_connect

#client.subscribe(TOPIC)
#client.subscribe("secure/files/response")

print("[RECEIVER] Waiting for files...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("[RECEIVER] Interrupted, exiting.")
