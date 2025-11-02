import os
import cohere
from dotenv import load_dotenv
from chromadb.api.types import EmbeddingFunction
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
print("COHERE_API_KEY:", COHERE_API_KEY)

co = cohere.Client(COHERE_API_KEY)

def generate_embedding(text):
    response = co.embed(texts=[text], model="small")
    return response.embeddings[0]

class CohereEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input):
        response = co.embed(texts=input, model="small")
        return response.embeddings

embedding_function = CohereEmbeddingFunction()