from langchain_groq import ChatGroq
from .config import GROQ_API_KEY

def ask_question(question: str, context: str):

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = f"""
    Answer the question using only the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content