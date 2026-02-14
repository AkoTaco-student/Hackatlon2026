import paho.mqtt.client as mqtt
import ssl
import base64
import os
import sys
import uuid
import socket

# ================= CONFIG =================

BROKER = os.environ.get("BROKER_HOST") or (sys.argv[1] if len(sys.argv) > 1 else "HackatlonServer")
BROKER_HOST = os.environ.get("BROKER_HOST", "HackatlonServer")

PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"

# Unique client ID (important for multi-computer setup)
CLIENT_ID = f"client_{socket.gethostname()}_{uuid.uuid4().hex[:6]}"
RESPONSE_TOPIC = f"secure/files/response/{CLIENT_ID}"

# ==========================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[CLIENT] Connected successfully")
        client.subscribe(RESPONSE_TOPIC)
        print(f"[CLIENT] Subscribed to {RESPONSE_TOPIC}")
    else:
        print("[CLIENT] Connection failed:", rc)

def on_message(client, userdata, msg):
    print("[CLIENT] AI response received!")

    try:
        filename, encoded = msg.payload.decode().split("::")
        file_data = base64.b64decode(encoded)

        save_name = "response_" + filename

        with open(save_name, "wb") as f:
            f.write(file_data)

        print(f"[CLIENT] Saved as {save_name}")
    except Exception as e:
        print("[CLIENT ERROR]", e)

    client.disconnect()

def send_file(client, filepath):
    with open(filepath, "rb") as f:
        file_data = f.read()

    encoded = base64.b64encode(file_data).decode()

    payload = f"{os.path.basename(filepath)}::{CLIENT_ID}::{encoded}"

    client.publish(REQUEST_TOPIC, payload)
    print("[CLIENT] File sent to AI")

# ================= MAIN =================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python secure_client.py <file_to_send>")
        sys.exit(1)

    filepath = sys.argv[1]

    client = mqtt.Client(client_id=CLIENT_ID)

    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print("[CLIENT] Connecting...")
    client.connect(BROKER, PORT)

    client.loop_start()

    # Give time to connect & subscribe
    import time
    time.sleep(1)

    send_file(client, filepath)

    # Wait until response received
    while client.is_connected():
        time.sleep(0.5)

    print("[CLIENT] Done.")