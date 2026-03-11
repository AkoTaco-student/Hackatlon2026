# pip install langchain langchain-community chromadb sentence-transformers pypdf langchain-huggingface paho-mqtt
# Written by: 
__author__ = "Cache Me if You Can"

import paho.mqtt.client as mqtt
import ssl
import base64
import os

# ---------------- LangChain RAG imports ----------------
from langchain_community.llms import Ollama
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ---------------- MQTT CONFIG ----------------

BROKER = "HackatlonServer"
#BROKER = "127.0.0.1"
PORT = 8883

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CA_CERT = os.path.join(BASE_DIR, "certs", "ca_dir", "ec_ca_cert.pem")
CLIENT_CERT = os.path.join(BASE_DIR, "certs", "client", "ec_client_cert.pem")
CLIENT_KEY = os.path.join(BASE_DIR, "certs", "client", "ec_client_private.pem")

REQUEST_TOPIC = "secure/files/request"

# ---------------- RAG SETUP ----------------

def load_rag_documents(folder_path):
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            if filename.endswith(".txt"):
                loader = TextLoader(
                    file_path,
                    encoding="utf-8",
                    autodetect_encoding=True
                )
                documents.extend(loader.load())
                print(f"[AI] Loaded TXT: {filename}")

            elif filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents.extend(loader.load())
                print(f"[AI] Loaded PDF: {filename}")

        except Exception as e:
            print(f"[AI] ⚠️ Could not load {filename}: {e}")

    print(f"[AI] Total documents loaded: {len(documents)}")
    return documents


print("[AI] Loading RAG documents...")
RAG_FOLDER = os.path.join(BASE_DIR, "rag")
documents = load_rag_documents(RAG_FOLDER)

# Split text
text_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
texts = text_splitter.split_documents(documents)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector DB
db = Chroma.from_documents(texts, embeddings)

# LLM
llm = Ollama(
    model="llama3",
    temperature=0.2,
    num_predict=300
)   

print("[AI] RAG system ready!")

# ---------------- MQTT CALLBACKS ----------------

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[AI] Connected to broker!")
        client.subscribe(REQUEST_TOPIC)
        print(f"[AI] Subscribed to {REQUEST_TOPIC}")
    else:
        print("[AI] Connection failed with code:", rc)


def on_message(client, userdata, msg):
    print("[AI] Query received")

    try:
        parts = msg.payload.decode().split("::")

        # filename::client_id::request_id::base64data
        if len(parts) != 4:
            print("[AI ERROR] Invalid payload format:", parts)
            return

        filename, client_id, request_id, encoded = parts

        file_data = base64.b64decode(encoded)
        query = file_data.decode(errors="ignore")

        print("[AI] Searching knowledge base...")
        docs = db.similarity_search(query, k=3)

        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"""
            Svar kort og presist.

            Kontekst:
            {context[:1500]}

            Spørsmål:
            {query}
            """

        print("[AI] Sending to LLM...")
        result = llm.invoke(prompt)

        response_filename = "ai_response_" + filename


        with open(response_filename, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"[AI] Response saved locally as: {response_filename}")


        encoded_response = base64.b64encode(
            result.encode("utf-8")
        ).decode("utf-8")


        payload = f"{request_id}::{response_filename}::{encoded_response}"

        response_topic = f"secure/files/response/{client_id}"
        client.publish(response_topic, payload)

        print("[AI] Response sent!")
        print(f"[AI] Topic: {response_topic}")

    except Exception as e:
        print("[AI ERROR]", e)


# ---------------- MQTT CLIENT ----------------

client = mqtt.Client(protocol=mqtt.MQTTv311)


client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_connect = on_connect
client.on_message = on_message

print("[AI] Connecting...")
client.connect(BROKER, PORT)

print("[AI] Waiting for queries...")
client.loop_forever()