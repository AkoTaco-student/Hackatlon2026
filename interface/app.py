"""
Flask backend for AI Chat interface
Connects to Ollama LLM service
"""

from flask import Flask, request, jsonify, Response, send_from_directory, stream_with_context
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app)

# Ollama API endpoint (default: localhost:11434)
OLLAMA_API = os.environ.get('OLLAMA_API', 'http://localhost:11434')
MODEL_NAME = os.environ.get('MODEL_NAME', 'llama2')

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
        timeout=30
    )
    if resp.status_code >= 400:
        return jsonify({'error': resp.text}), resp.status_code
    data = resp.json()
    return jsonify({
        'session_id': (data.get('data') or {}).get('session_id') or data.get('session_id'),
        'session_token': (data.get('data') or {}).get('session_token') or data.get('session_token')
    })

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
