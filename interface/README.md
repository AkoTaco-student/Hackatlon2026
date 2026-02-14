# AI Chat Interface

Et chat-interface som kobler seg til Ollama AI-modeller (f.eks. Llama 3).

## Setup

### 1. Installér dependencies

```powershell
pip install flask flask-cors requests
```

### 2. Start Ollama (hvis ikke allerede kjørende)

```powershell
ollama serve
# Eller i en annen terminal:
ollama run llama3
```

Ollama må kjøre på `http://localhost:11434` (default).

### 3. Start Flask backend

Fra `interface/` mappen:

```powershell
python app.py
```

Server starter på: `http://localhost:5000`

### 4. Åpne browser

Åpne `http://localhost:5000` i en nettleser og begynn å chatte!

## Miljøvariabler

Du kan angi disse før kjøring:

```powershell
$env:OLLAMA_API = "http://localhost:11434"  # Ollama API URL
$env:MODEL_NAME = "llama3"                   # Modellnavn (default: llama2)
$env:HEYGEN_API_KEY = "your_heygen_api_key"  # HeyGen API key
$env:HEYGEN_AVATAR_ID = "your_avatar_id"     # HeyGen avatar id
$env:HEYGEN_VOICE_ID = "your_voice_id"       # (valgfritt) voice id
$env:D_ID_API_KEY = "optional"               # (valgfritt) fallback


python app.py
```

## Feilsøking

**Feil: "Cannot connect to Ollama"**

- Sjekk at Ollama kjører: `ollama serve` eller `ollama run llama3`
- Sjekk at den kjører på `localhost:11434`

**Feil: "Model not found"**

- Installer modellen: `ollama pull llama3`

**Port 5000 allerede i bruk:**

- Endre port i `app.py` eller stop annen prosess

## API Endpoints

- `POST /api/chat` - Send melding, få svar fra AI
- `POST /api/chat/stream` - Stream svar med SSE
- `GET /api/models` - Liste over tilgjengelige modeller
- `GET /health` - Helsesjekk
- `POST /api/heygen/token` - Hent HeyGen token (brukes av frontend)

## Filer

- `index.html` - Chat-grensesnitt
- `styles.css` - Styling
- `chat.js` - Frontend JavaScript
- `avatarStream.js` - HeyGen avatar streaming
- `avatar-test.html` - Enkel testside for avatar
- `avatar-test.js` - Testlogikk
- `app.py` - Flask backend
