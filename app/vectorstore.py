from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from .config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from .embeddings import get_embeddings

def get_vectorstore(namespace:str):

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine"
        )

    embeddings = get_embeddings()       
    return PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
        namespace=namespace
    )