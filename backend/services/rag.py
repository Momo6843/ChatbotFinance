from backend.db.chroma import vector_collection
from backend.services.embeddings import generate_embedding
import cohere
from dotenv import load_dotenv
import os

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(COHERE_API_KEY)

def retrieve_context(question, pdf_filter=None, page_filter=None, tag_filter=None, top_k=5):
    filters = {}
    if pdf_filter:
        filters['document_name'] = pdf_filter
    if page_filter:
        filters['page_number'] = {"$in": page_filter}
    if tag_filter:
        filters['tags'] = tag_filter

    results = vector_collection.query(
        query_texts=[question],
        n_results=top_k,
        where=filters if filters else None
    )
    context_texts = []
    context_meta = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        context_texts.append(doc)
        context_meta.append({"pdf": meta.get("document_name"), "pages": meta.get("page_number")})
    return context_texts, context_meta

def generate_answer(question, context_texts):
    # Improved prompt for better RAG performance
    context = "\n---\n".join(context_texts)
    prompt = (
        "Tu es un assistant expert en sociologie des organisation . Réponds de façon claire et directe à la question ci-dessous en utilisant uniquement le contexte fourni. "
    "Si la réponse n'est pas dans le contexte, dis simplement : 'Je n'ai pas cette information.'\n"
    f"VOICI LE Question utilisateur : {question}\n VOICI Le Contexte:\n{context}\n\n Réponse :"
    )
    response = co.chat(
        model="command-a-03-2025",  # Remplace par le modèle recommandé par Cohere si nécessaire
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.message.content[0].text
