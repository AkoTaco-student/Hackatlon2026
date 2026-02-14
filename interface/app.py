"""
Flask backend for AI Chat interface
Connects to Ollama LLM service
"""

from flask import Flask, request, jsonify, Response, send_from_directory, stream_with_context
from flask_cors import CORS
import requests
import os
import json
import time

app = Flask(__name__)
CORS(app)

# Ollama API endpoint (default: localhost:11434)
OLLAMA_API = os.environ.get('OLLAMA_API', 'http://localhost:11434')
MODEL_NAME = os.environ.get('MODEL_NAME', 'llama2')

# HeyGen Streaming Avatar (preferred)
HEYGEN_API_KEY = os.environ.get('HEYGEN_API_KEY')
HEYGEN_AVATAR_ID = os.environ.get('HEYGEN_AVATAR_ID', '')
HEYGEN_VOICE_ID = os.environ.get('HEYGEN_VOICE_ID', '')
HEYGEN_BASE_URL = os.environ.get('HEYGEN_BASE_URL', 'https://api.heygen.com')

# D-ID fallback (optional)
D_ID_API_KEY = os.environ.get('D_ID_API_KEY')
D_ID_AGENT_ID = os.environ.get('D_ID_AGENT_ID', '')

# In-memory session token cache for HeyGen
_HEYGEN_SESSION_TOKENS = {}


@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(os.path.dirname(__file__), path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages and return AI responses
    """
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Call Ollama API
        response = call_ollama(user_message)
        
        return jsonify({
            'response': response,
            'model': MODEL_NAME
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """
    Stream chat responses from Ollama as SSE
    """
    data = request.json or {}
    user_message = (data.get('message') or '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    def generate():
        try:
            for chunk in call_ollama_stream(user_message):
                yield f"data: {json.dumps({'type': 'chunk', 'text': chunk})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

def call_ollama(prompt):
    """
    Call Ollama API and get response from Høyre's perspective
    """
    try:
        url = f'{OLLAMA_API}/api/generate'
        
        # System prompt to make AI respond from Høyre's perspective
        system_prompt = """Du er en representant for Høyre, Norges klassisk konservative høyreparti. 
Du argumenterer for:
- Mindre stat og større frihet for enkeltindividet
- Fritt marked og privat initiativ
- Sterk kjernefamilie og kulturelle tradisjoner
- Nasjonal selvbestemmelse og sikkerhet
- Privat ansvar og gjensidig hjelp
- Effektiv offentlig sektor

Svar på norsk, vær høflig men selvsikker i dine standpunkter. Du representerer liberal-konservativ politikk."""
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nHøyre-representant:"
        
        payload = {
            'model': MODEL_NAME,
            'prompt': full_prompt,
            'stream': False,
            'temperature': 0.7
        }
        
        print(f"[Ollama] Calling {url} with model: {MODEL_NAME}")
        print(f"[User] {prompt}")
        
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result.get('response', 'No response from model').strip()
        
        print(f"[AI] {ai_response}")
        
        return ai_response
    
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to Ollama at {OLLAMA_API}. Is it running?")
    except requests.exceptions.Timeout:
        raise Exception("Ollama request timed out. Try a simpler question.")
    except Exception as e:
        raise Exception(f"Ollama error: {str(e)}")


def call_ollama_stream(prompt):
    """
    Call Ollama API with stream=True and yield text chunks
    """
    url = f'{OLLAMA_API}/api/generate'
    system_prompt = """Du er en representant for Høyre, Norges klassisk konservative høyreparti. 
Du argumenterer for:
- Mindre stat og større frihet for enkeltindividet
- Fritt marked og privat initiativ
- Sterk kjernefamilie og kulturelle tradisjoner
- Nasjonal selvbestemmelse og sikkerhet
- Privat ansvar og gjensidig hjelp
- Effektiv offentlig sektor

Svar på norsk, vær høflig men selvsikker i dine standpunkter. Du representerer liberal-konservativ politikk."""
    full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nHøyre-representant:"

    payload = {
        'model': MODEL_NAME,
        'prompt': full_prompt,
        'stream': True,
        'temperature': 0.7
    }

    response = requests.post(url, json=payload, timeout=300, stream=True)
    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        data = json.loads(line.decode('utf-8'))
        if data.get('done'):
            break
        chunk = data.get('response', '')
        if chunk:
            yield chunk


@app.route('/api/avatar/config', methods=['GET'])
def avatar_config():
    """
    Provide frontend config without exposing API keys
    """
    provider = 'heygen' if HEYGEN_API_KEY else ('d-id' if D_ID_API_KEY else 'none')
    return jsonify({
        'provider': provider,
        'heygen': {
            'avatar_id': HEYGEN_AVATAR_ID,
            'voice_id': HEYGEN_VOICE_ID
        },
        'd_id': {
            'agent_id': D_ID_AGENT_ID
        }
    })


def _heygen_create_token():
    if not HEYGEN_API_KEY:
        raise Exception('HEYGEN_API_KEY is not set')
    resp = requests.post(
        f'{HEYGEN_BASE_URL}/v1/streaming.create_token',
        headers={'x-api-key': HEYGEN_API_KEY},
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    token = data.get('data', {}).get('token') or data.get('token')
    if not token:
        raise Exception('Failed to obtain HeyGen token')
    return token


@app.route('/api/heygen/token', methods=['POST'])
def heygen_token():
    """
    Return a short-lived HeyGen token for browser SDK usage
    """
    try:
        token = _heygen_create_token()
        return jsonify({'token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/heygen/session', methods=['POST'])
def heygen_session():
    """
    Create and start a HeyGen streaming session
    """
    if not HEYGEN_API_KEY:
        return jsonify({'error': 'HEYGEN_API_KEY is not set'}), 400
    body = request.json or {}
    avatar_id = body.get('avatar_id') or HEYGEN_AVATAR_ID
    if not avatar_id:
        return jsonify({'error': 'HEYGEN_AVATAR_ID is not set'}), 400

    token = _heygen_create_token()

    new_resp = requests.post(
        f'{HEYGEN_BASE_URL}/v1/streaming.new',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'version': 'v2',
            'avatar_id': avatar_id,
            'voice_id': HEYGEN_VOICE_ID or None
        },
        timeout=30
    )
    new_resp.raise_for_status()
    session_info = new_resp.json()

    start_resp = requests.post(
        f'{HEYGEN_BASE_URL}/v1/streaming.start',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'session_id': session_info.get('session_id')
        },
        timeout=30
    )
    start_resp.raise_for_status()

    session_id = session_info.get('session_id')
    if session_id:
        _HEYGEN_SESSION_TOKENS[session_id] = {
            'token': token,
            'created_at': time.time()
        }

    return jsonify({
        'session': session_info
    })


@app.route('/api/heygen/task', methods=['POST'])
def heygen_task():
    """
    Send text to HeyGen avatar
    """
    body = request.json or {}
    session_id = body.get('session_id')
    text = (body.get('text') or '').strip()
    task_type = body.get('task_type') or 'repeat'

    if not session_id or not text:
        return jsonify({'error': 'session_id and text are required'}), 400

    session = _HEYGEN_SESSION_TOKENS.get(session_id)
    if not session:
        return jsonify({'error': 'Unknown or expired session'}), 400

    token = session['token']
    resp = requests.post(
        f'{HEYGEN_BASE_URL}/v1/streaming.task',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={
            'session_id': session_id,
            'text': text,
            'task_type': task_type
        },
        timeout=30
    )
    if resp.status_code >= 400:
        return jsonify({'error': resp.text}), resp.status_code
    return jsonify({'ok': True})


@app.route('/api/heygen/stop', methods=['POST'])
def heygen_stop():
    body = request.json or {}
    session_id = body.get('session_id')
    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400

    session = _HEYGEN_SESSION_TOKENS.get(session_id)
    if not session:
        return jsonify({'error': 'Unknown or expired session'}), 400

    token = session['token']
    resp = requests.post(
        f'{HEYGEN_BASE_URL}/v1/streaming.stop',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        },
        json={'session_id': session_id},
        timeout=30
    )
    if resp.status_code >= 400:
        return jsonify({'error': resp.text}), resp.status_code

    _HEYGEN_SESSION_TOKENS.pop(session_id, None)
    return jsonify({'ok': True})

@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Get list of available Ollama models
    """
    try:
        url = f'{OLLAMA_API}/api/tags'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        models = response.json().get('models', [])
        return jsonify({'models': models})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """
    Health check - verify Ollama connection
    """
    try:
        url = f'{OLLAMA_API}/api/tags'
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        
        return jsonify({
            'status': 'healthy',
            'ollama': 'connected',
            'model': MODEL_NAME
        })
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'ollama': 'disconnected',
            'error': str(e)
        }), 503

if __name__ == '__main__':
    print(f"Starting Høyre AI Chat Interface...")
    print(f"Ollama API: {OLLAMA_API}")
    print(f"Model: {MODEL_NAME}")
    print(f"Open http://localhost:5000 in your browser")
    print(f"")
    print(f"🇳🇴 Høyre - Med mindre stat, frihet og ansvar")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )
