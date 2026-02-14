#   pip install langchain langchain-community chromadb sentence-transformers pypdf


import paho.mqtt.client as mqtt
import ssl
import base64
import os
import requests

# LangChain RAG imports
from langchain_community.llms import Ollama
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings



# ---------------- MQTT CONFIG ----------------

BROKER = "HackatlonServer"
PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"
RESPONSE_TOPIC = "secure/files/response"

# ---------------- RAG SETUP ----------------

print("[AI] Loading RAG documents...")

RAG_FOLDER = os.path.join(BASE_DIR, "rag")

documents = []

for file in os.listdir(RAG_FOLDER):
    path = os.path.join(RAG_FOLDER, file)

    if file.endswith(".txt"):
        loader = TextLoader(path)
        documents.extend(loader.load())

    elif file.endswith(".pdf"):
        loader = PyPDFLoader(path)
        documents.extend(loader.load())

print(f"[AI] Loaded {len(documents)} documents")

# Split text
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Embeddings
#embeddings = HuggingFaceEmbeddings()
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# Vector DB
db = Chroma.from_documents(texts, embeddings)

# LLM
#llm = Ollama(model="llama3")
llm = Ollama(
    model="llama3",
    temperature=0.2,
    num_predict=300
)

print("[AI] RAG system ready!")

# ---------------- MQTT CALLBACK ----------------

def on_message(client, userdata, msg):
    print("[AI] Query received")

    try:
        filename, client_id, encoded = msg.payload.decode().split("::")
        file_data = base64.b64decode(encoded)
        query = file_data.decode(errors="ignore")

        print("[AI] Searching knowledge base...")
        docs = db.similarity_search(query, k=3)

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
Svar på spørsmålet basert på kontekst.

Kontekst:
{context}

Spørsmål:
{query}
"""

        print("[AI] Sending to LLM...")
        result = llm.invoke(prompt)

        response_filename = "ai_response_" + filename

        encoded_response = base64.b64encode(
            result.encode()
        ).decode()

        payload = response_filename + "::" + encoded_response

        #client.publish(RESPONSE_TOPIC, payload, retain=True)
        response_topic = f"secure/files/response/{client_id}"
        client.publish(response_topic, payload)
        print("[AI] Response sent!")

    except Exception as e:
        print("[AI ERROR]", e)


# ---------------- MQTT CLIENT ----------------

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

print("[AI] Waiting for queries...")
client.loop_forever()





"""

    print("[AI] Sending to Ollama...")
    response = llm.invoke(prompt)

    response_filename = "ai_response_" + filename

    encoded_response = base64.b64encode(
        response.encode()
    ).decode()

    payload = response_filename + "::" + encoded_response

    client.publish(RESPONSE_TOPIC, payload)

    print("[AI] Response sent!")

# ---------------- MQTT START ----------------

client = mqtt.Client()
client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_message = on_message

print("[AI] Connecting to broker...")
client.connect(BROKER, PORT)

client.subscribe(REQUEST_TOPIC)

print("[AI] Waiting for queries...")
client.loop_forever()
"""


"""
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




