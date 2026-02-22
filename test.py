import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# 1️⃣ Load PDFs
def read_doc(directory):
    loader = PyPDFDirectoryLoader(directory)
    return loader.load()

# 2️⃣ Split text
def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)

documents = read_doc("documents/")
docs = chunk_data(documents)

# 3️⃣ Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4️⃣ Connect Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")

# 5️⃣ Create index if not exists
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine"
    )

# 6️⃣ Upload documents
vectorstore = PineconeVectorStore.from_documents(
    docs,
    embeddings,
    index_name=index_name
)

print("✅ Ingestion Complete")