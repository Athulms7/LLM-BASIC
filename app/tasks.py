from app.celery import celery
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from app.vectorstore import get_vectorstore
import tempfile
import os

@celery.task
def process_pdf_task(file_bytes, user_id):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name

    loader = PyPDFLoader(temp_path)
    documents = loader.load()
    os.remove(temp_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    docs = splitter.split_documents(documents)

    vectorstore = get_vectorstore(namespace=user_id)
    vectorstore.add_documents(docs)

    return "Processing complete"