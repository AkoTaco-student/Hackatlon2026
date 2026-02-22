import paho.mqtt.client as mqtt
import ssl
import base64
import os
import socket
import tempfile
import threading

BROKER = "HackatlonServer"
PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"
CLIENT_ID = f"client_{socket.gethostname()}_{os.getpid()}"
RESPONSE_TOPIC = f"secure/files/response/{CLIENT_ID}"


def send_file_and_wait(filepath, timeout=30):
    """
    Sends file to MQTT TLS server and waits for response.
    Returns response file content as string.
    """

    response_data = {"content": None}
    finished = threading.Event()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(RESPONSE_TOPIC)
            send_file(client)

    def on_message(client, userdata, msg):
        try:
            filename, encoded = msg.payload.decode().split("::")
            file_data = base64.b64decode(encoded)
            response_data["content"] = file_data.decode(errors="ignore")
        except Exception as e:
            response_data["content"] = f"ERROR: {str(e)}"
        finally:
            finished.set()
            client.disconnect()

    def send_file(client):
        with open(filepath, "rb") as f:
            file_data = f.read()

        encoded = base64.b64encode(file_data).decode()
        payload = f"{os.path.basename(filepath)}::{CLIENT_ID}::{encoded}"
        client.publish(REQUEST_TOPIC, payload)

    client = mqtt.Client(client_id=CLIENT_ID)

    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT)
    client.loop_start()

    finished.wait(timeout=timeout)
    client.loop_stop()

    return response_data["content"]