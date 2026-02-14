import paho.mqtt.client as mqtt
import ssl
import base64
import os
import sys
import socket

# ================= CONFIG =================

BROKER = "HackatlonServer"
PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"

# 🔒 STABIL CLIENT ID (ikke random!)
CLIENT_ID = f"client_{socket.gethostname()}"
RESPONSE_TOPIC = f"secure/files/response/{CLIENT_ID}"

FILE_TO_SEND = None

# ==========================================

def send_file(client):
    with open(FILE_TO_SEND, "rb") as f:
        file_data = f.read()

    encoded = base64.b64encode(file_data).decode()

    payload = f"{os.path.basename(FILE_TO_SEND)}::{CLIENT_ID}::{encoded}"

    client.publish(REQUEST_TOPIC, payload)
    print("[CLIENT] File sent to AI")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[CLIENT] Connected successfully")
        print("[CLIENT] CLIENT_ID:", CLIENT_ID)

        client.subscribe(RESPONSE_TOPIC)
        print(f"[CLIENT] Subscribed to {RESPONSE_TOPIC}")

        # Send file AFTER subscribe
        send_file(client)
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


# ================= MAIN =================

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python secure_client.py <file_to_send>")
        sys.exit(1)

    FILE_TO_SEND = sys.argv[1]

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

    client.loop_forever()

    print("[CLIENT] Done.")