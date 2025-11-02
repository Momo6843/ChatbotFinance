import os
from dotenv import load_dotenv
import chromadb
from backend.services.embeddings import embedding_function

load_dotenv()
chroma_dir = os.getenv("CHROMA_DIR", "./chroma_db")
chroma_client = chromadb.PersistentClient(path=chroma_dir)

vector_collection = chroma_client.create_collection(
    name="documents_v384",
    embedding_function=embedding_function,
    get_or_create=True
)
