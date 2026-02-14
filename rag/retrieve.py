from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embedding = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding
)

query = "Hva handler dokumentet om?"

docs = vectorstore.similarity_search(query, k=3)

for i, doc in enumerate(docs):
    print(f"\nResultat {i+1}:\n")
    print(doc.page_content)
