"""
Flask backend for AI Chat interface
Connects to Ollama LLM service
"""
import uuid

from flask import Response, stream_with_context
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json


import sys
import paho.mqtt.client as mqtt
import ssl
import base64
import threading
import socket

import tempfile

# ================= MQTT CONFIG =================
BROKER = "HackatlonServer"
#BROKER = "127.0.0.1"

PORT = 8883

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

CLIENT_ID = f"flask_server_{socket.gethostname()}"
REQUEST_TOPIC = "secure/files/request"
RESPONSE_TOPIC = f"secure/files/response/{CLIENT_ID}"

mqtt_client = None
mqtt_response = {"data": None}
mqtt_event = threading.Event()

app = Flask(__name__)
CORS(app)

pending_requests = {}
# LiveAvatar (current)
LIVEAVATAR_API_KEY = os.environ.get('LIVEAVATAR_API_KEY')
LIVEAVATAR_AVATAR_ID = os.environ.get('LIVEAVATAR_AVATAR_ID', '')
LIVEAVATAR_VOICE_ID = os.environ.get('LIVEAVATAR_VOICE_ID', '')
LIVEAVATAR_CONTEXT_ID = os.environ.get('LIVEAVATAR_CONTEXT_ID', '')
LIVEAVATAR_LANGUAGE = os.environ.get('LIVEAVATAR_LANGUAGE', 'no')
LIVEAVATAR_MODE = os.environ.get('LIVEAVATAR_MODE', 'FULL')
LIVEAVATAR_API_URL = os.environ.get('LIVEAVATAR_API_URL', 'https://api.liveavatar.com')
LIVEAVATAR_SANDBOX = os.environ.get('LIVEAVATAR_SANDBOX', 'false').lower() in ['1', 'true', 'yes']


@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.dirname(__file__), path)

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message")

    def generate():
        
        request_id = str(uuid.uuid4())

        event = threading.Event()
        response_holder = {"data": None}

        pending_requests[request_id] = {
            "event": event,
            "response": response_holder}
        

        mqtt_event.clear()
        mqtt_response["data"] = None

        encoded = base64.b64encode(user_message.encode()).decode()
        payload = f"prompt.txt::{CLIENT_ID}::{request_id}::{encoded}"

        mqtt_client.publish(REQUEST_TOPIC, payload)
        print("[MQTT] Prompt sent")

        mqtt_event.wait(timeout=45)

        ai_response = mqtt_response["data"]
        if not event.wait(timeout=45):
            yield f"data: {json.dumps({'type':'error','error':'Timeout'})}\n\n"
            return

        ai_response = response_holder["data"]
        del pending_requests[request_id]


        if not ai_response:
            yield f"data: {json.dumps({'type':'error','error':'No response'})}\n\n"
            return

        words = ai_response.split(" ")

        for word in words:
            chunk = {"type": "chunk", "text": word + " "}
            yield f"data: {json.dumps(chunk)}\n\n"

        yield f"data: {json.dumps({'type':'done'})}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream"
    )

def call_ollama(prompt):

    mqtt_event.clear()
    mqtt_response["data"] = None

    encoded = base64.b64encode(prompt.encode()).decode()
    payload = f"prompt.txt::{CLIENT_ID}::{encoded}"

    mqtt_client.publish(REQUEST_TOPIC, payload)

    print("[MQTT] Prompt sent")

    mqtt_event.wait(timeout=45)
    return mqtt_response["data"] or "No response received"


@app.route('/api/avatar/config', methods=['GET'])
def avatar_config():
    """
    Provide frontend config without exposing API keys
    """
    provider = 'liveavatar' if LIVEAVATAR_API_KEY else 'none'
    return jsonify({
        'provider': provider,
        'liveavatar': {
            'avatar_id': LIVEAVATAR_AVATAR_ID,
            'voice_id': LIVEAVATAR_VOICE_ID,
            'context_id': LIVEAVATAR_CONTEXT_ID,
            'language': LIVEAVATAR_LANGUAGE,
            'mode': LIVEAVATAR_MODE,
            'is_sandbox': LIVEAVATAR_SANDBOX,
            'api_url': LIVEAVATAR_API_URL
        }
    })

@app.route('/api/liveavatar/token', methods=['POST'])
def liveavatar_token():
    """
    Create a LiveAvatar session token
    """
    if not LIVEAVATAR_API_KEY:
        return jsonify({'error': 'LIVEAVATAR_API_KEY is not set'}), 400
    if not LIVEAVATAR_AVATAR_ID:
        return jsonify({'error': 'LIVEAVATAR_AVATAR_ID is not set'}), 400
    if not LIVEAVATAR_VOICE_ID:
        return jsonify({'error': 'LIVEAVATAR_VOICE_ID is not set'}), 400

    payload = {
        'mode': LIVEAVATAR_MODE,
        'avatar_id': LIVEAVATAR_AVATAR_ID,
        'avatar_persona': {
            'voice_id': LIVEAVATAR_VOICE_ID,
            'language': LIVEAVATAR_LANGUAGE
        }
    }
    if LIVEAVATAR_CONTEXT_ID:
        payload['avatar_persona']['context_id'] = LIVEAVATAR_CONTEXT_ID
    if LIVEAVATAR_SANDBOX:
        payload['is_sandbox'] = True

    resp = requests.post(
        f'{LIVEAVATAR_API_URL}/v1/sessions/token',
        headers={
            'X-API-KEY': LIVEAVATAR_API_KEY,
            'accept': 'application/json',
            'content-type': 'application/json'
        },
        json=payload,
        timeout=45
    )
    if resp.status_code >= 400:
        return jsonify({'error': resp.text}), resp.status_code
    data = resp.json()
    return jsonify({
        'session_id': (data.get('data') or {}).get('session_id') or data.get('session_id'),
        'session_token': (data.get('data') or {}).get('session_token') or data.get('session_token')
    })
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected")
        client.subscribe(RESPONSE_TOPIC)
        print(f"[MQTT] Subscribed to {RESPONSE_TOPIC}")
    else:
        print("[MQTT] Connection failed:", rc)

def on_message(client, userdata, msg):
    try:
        parts = msg.payload.decode().split("::")

        if len(parts) != 3:
            print("[MQTT] Invalid response format:", parts)
            return

        request_id, filename, encoded = parts

        decoded = base64.b64decode(encoded).decode(errors="ignore")

        if request_id in pending_requests:
            pending_requests[request_id]["response"]["data"] = decoded
            pending_requests[request_id]["event"].set()

    except Exception as e:
        print("[MQTT] Error:", e)

        
def start_mqtt():
    global mqtt_client

    mqtt_client = mqtt.Client(client_id=CLIENT_ID)

    mqtt_client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(BROKER, PORT)
    mqtt_client.loop_start()

if __name__ == '__main__':
    start_mqtt()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
