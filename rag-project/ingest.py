import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# 1️ Load dokument
loader = PyPDFLoader("/dokuments/Hoyres-klimameny-PDF.pdf")
documents = loader.load()

print(f"Antall sider lastet: {len(documents)}")

# 2️ Chunk dokument
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print(f"Antall chunks: {len(chunks)}")

# 3️ Se eksempel
print(chunks[0].page_content)
