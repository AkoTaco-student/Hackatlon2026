import paho.mqtt.client as mqtt
import ssl
import base64
import sys
import os

BROKER = os.environ.get("BROKER_HOST") or (sys.argv[1] if len(sys.argv) > 1 else "HackatlonServer")
BROKER_HOST = os.environ.get("BROKER_HOST", "HackatlonServer")
PORT = 8883


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

TOPIC = "secure/files"


def send_file(filename):
    client = mqtt.Client()
    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    print("[CLIENT] Connecting...")
    client.connect(BROKER, PORT)
    client.loop_start()

    with open(filename, "rb") as f:
        file_data = f.read()

    encoded = base64.b64encode(file_data).decode()

    payload = os.path.basename(filename) + "::" + encoded

    client.publish(TOPIC, payload)
    print("[CLIENT] File sent!")

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    send_file(sys.argv[1]) # Example only
    #send_file(r"C:\Users\Akos\Documents\myfile.txt") --- We are gonna use this
