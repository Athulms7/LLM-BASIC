from fastapi import FastAPI, UploadFile, File
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from app.vectorstore import get_vectorstore
from app.rag import ask_question
from app.tasks import process_pdf_task
from app.types import QueryRequest

app = FastAPI()

@app.post("/upload")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):

    file_bytes = await file.read()

    # Send to queue instead of processing
    task=process_pdf_task.delay(file_bytes, user_id)

    return {"task_id": task.id}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    task = process_pdf_task.AsyncResult(task_id)
    return {"status": task.status}
import time
@app.post("/ask")
def ask(request: QueryRequest):

    vectorstore = get_vectorstore(namespace=request.user_id)

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    start=time.time()
    docs = retriever.invoke(request.question)
    print("Retrival time:", time.time() - start)
    if not docs:
        return {"answer": "No relevant information found."}

    context = "\n\n".join([doc.page_content for doc in docs])
    start=time.time()
    answer = ask_question(request.question, context)
    print("LLM time:", time.time() - start) 

    return {"answer": answer}



# -----------------------
# Upload PDF Endpoint
# -----------------------

# @app.post("/upload")
# async def upload_pdf(user_id: str, file: UploadFile = File(...)):

#     # Save temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         tmp.write(await file.read())
#         temp_path = tmp.name

#     # Load PDF
#     loader = PyPDFLoader(temp_path)
#     documents = loader.load()

#     os.remove(temp_path)

#     # Split
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=700,
#         chunk_overlap=200
#     )
#     docs = splitter.split_documents(documents)

#     # Add user metadata
    

#     for doc in docs:
#         doc.metadata["user_id"] = user_id

#     # Store in vector DB
#     vectorstore = get_vectorstore()
#     vectorstore.add_documents(docs,namespace=user_id)

#     return {"message": "PDF uploaded and indexed successfully"}


