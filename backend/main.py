from fastapi import FastAPI
from backend.routes import upload, chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Assistant IA PDF")

# Autoriser toutes les origines (ou adapte à ton domaine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:8501"] pour Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(upload.router)
app.include_router(chat.router)
