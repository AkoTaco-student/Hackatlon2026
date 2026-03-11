#!/usr/bin/env python3
"""
Secure MQTT Client using Mutual TLS (mTLS)
Publishes a file transfer request securely to Mosquitto
"""

import paho.mqtt.client as mqtt
import ssl
import os
import sys

# ===== CONFIGURATION =====

BROKER_HOST = "HackatlonServer"      # Use LAN IP if connecting from another computer
BROKER_PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT     = os.path.join(BASE_DIR, "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "client", "ec_client_cert.pem")
CLIENT_KEY  = os.path.join(BASE_DIR, "client", "ec_client_private.pem")

# ==========================


def send_file_command(filename):
    client = mqtt.Client()  # modern API (no deprecated version)

    # ---------- CALLBACKS ----------

    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("[CLIENT] Securely connected to broker")

            topic = f"files/send/{filename}"
            print(f"[CLIENT] Publishing to topic: {topic}")

            result = client.publish(topic, payload="transfer", qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("[CLIENT] Message published successfully")
            else:
                print("[CLIENT] Publish failed")

        else:
            print(f"[CLIENT] Connection failed with code: {rc}")

    def on_disconnect(client, userdata, rc, properties=None):
        print("[CLIENT] Disconnected from broker")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # ---------- TLS SETUP (Mutual TLS) ----------

    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    client.tls_insecure_set(False)  # Enforce certificate validation

    # ---------- CONNECT ----------

    print(f"[CLIENT] Connecting securely to {BROKER_HOST}:{BROKER_PORT}...")
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    client.loop_start()

    # Allow time for publish
    import time
    time.sleep(2)

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python secure_mqtt_client.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    send_file_command(filename)
