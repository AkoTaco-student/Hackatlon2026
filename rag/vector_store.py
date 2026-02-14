from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from ingest import chunks

# 1️ Embedding-modell fra Ollama
embedding = OllamaEmbeddings(model="llama3")

# 2️ Opprett vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./chroma_db"
)

# 3️ Lagre
vectorstore.persist()

print("Vector store opprettet med Ollama embeddings!")
