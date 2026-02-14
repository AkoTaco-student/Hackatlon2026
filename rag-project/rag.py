from langchain_community.llms import Ollama
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 1. Last dokument
loader = TextLoader("dokuments/syn-på-ki.txt")
documents = loader.load()

# 2. Del opp tekst
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 3. Embeddings
embeddings = HuggingFaceEmbeddings()

# 4. Vektordatabase
db = Chroma.from_documents(texts, embeddings)

# 5. LLM via Ollama
llm = Ollama(model="llama3")

# 6. Spørsmål
query = "Hva handler dokumentet om?"
docs = db.similarity_search(query)

context = "\n".join([doc.page_content for doc in docs])

prompt = f"""
Svar på spørsmålet basert på kontekst:

Kontekst:
{context}

Spørsmål:
{query}
"""

response = llm.invoke(prompt)
print(response)
