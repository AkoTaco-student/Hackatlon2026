import paho.mqtt.client as mqtt
import ssl
import base64
import os
import requests

BROKER = "HackatlonServer"
PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"
RESPONSE_TOPIC = "secure/files/response"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"   # change if needed


def process_with_ollama(text):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": text,
            "stream": False
        }
    )
    return response.json()["response"]


def on_message(client, userdata, msg):
    print("[AI] File received")

    filename, encoded = msg.payload.decode().split("::")
    file_data = base64.b64decode(encoded)

    text = file_data.decode(errors="ignore")

    print("[AI] Sending to Ollama...")
    result_text = process_with_ollama(text)

    response_filename = "ai_response_" + filename

    encoded_response = base64.b64encode(
        result_text.encode()
    ).decode()

    payload = response_filename + "::" + encoded_response

    client.publish(RESPONSE_TOPIC, payload)
    print("[AI] Response sent!")


client = mqtt.Client()
client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_message = on_message

print("[AI] Connecting...")
client.connect(BROKER, PORT)

client.subscribe(REQUEST_TOPIC)

print("[AI] Waiting for files...")
client.loop_forever()




























"""
import numpy as np
import nltk

from transformers import pipeline

nlp = pipeline("conversation", model= "distilberg-base-uncased")


def chatbot(text):
    # Implement your chatbot logic here
    pass

# Test the chatbot
chatbot("Hello, how are you?")

"""
""" Server.py ?"""
"""
from flask import Flask, request

app = Flask(__name__)

@app.route('/ping', methods=['POST'])
def ping_ai():
    # This function will be called when the AI sends a ping
    # You can use this opportunity to process data from another file
    return 'Ping received!'

if __name__ == '__main__':
    app.run(debug=True)


import requests

def ping_server():
    url = 'http://???'
    response = requests.post(url)
    if response.status_code == 200:
        # Data processing code goes here
        print('Ping received and processed!')
    else:
        print(f'Error: {response.status_code}')"""