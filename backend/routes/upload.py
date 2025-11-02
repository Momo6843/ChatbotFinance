from fastapi import APIRouter, UploadFile, File, Form
from backend.services.pdf_processor import extract_pages, chunk_pages
from backend.db.chroma import vector_collection
from backend.db.postgres import cursor, conn
from backend.services.embeddings import generate_embedding
import json  # Pour convertir les listes en string

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), doc_type: str = Form(...), tags: str = Form("")):
    pages = extract_pages(file.file)

    # Convertir les tags en string JSON pour Chroma
    tags_str = json.dumps([t.strip() for t in tags.split(",")]) if tags else ""

    if doc_type == "passager":
        for p in pages:
            embedding = generate_embedding(p['text'])
            vector_collection.add(
                documents=[p['text']],
                embeddings=[embedding],
                ids=[f"{file.filename}_{p['page_number']}"],
                metadatas=[{
                    "document_name": file.filename,
                    "page_number": p['page_number'],
                    "tags": tags_str
                }]
            )
        return {"message": "Document passager traité"}

    elif doc_type == "definitif":
        chunks = chunk_pages(pages, chunk_size=3)
        for chunk in chunks:
            embedding = generate_embedding(chunk['text'])
            vector_collection.add(
                documents=[chunk['text']],
                embeddings=[embedding],
                ids=[f"{file.filename}_{chunk['pages'][0]}"],
                metadatas=[{
                    "document_name": file.filename,
                    "page_number": json.dumps(chunk['pages']),  # Convertir la liste de pages en string JSON
                    "tags": tags_str
                }]
            )
        # Pour PostgreSQL, tu peux aussi stocker les tags comme string JSON
        cursor.execute(
            "INSERT INTO documents (filename, tags) VALUES (%s, %s)",
            (file.filename, tags_str)
        )
        conn.commit()
        return {"message": "Document définitif stocké"}
