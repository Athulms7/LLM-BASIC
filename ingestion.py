from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .app.vectorstore import get_vectorstore

def ingest_documents(directory="documents/"):

    loader = PyPDFDirectoryLoader(directory)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    vectorstore = get_vectorstore()
    vectorstore.add_documents(docs)

    return "✅ Ingestion Complete"