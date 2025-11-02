import streamlit as st
import requests


import os
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Assistant IA", layout="wide", page_icon="🤖")
st.markdown("""
<style>
.sidebar .sidebar-content {width: 350px;}
</style>
""", unsafe_allow_html=True)

# Sidebar: historique + upload
with st.sidebar:
    st.title("🕒 Historique & Upload")
    st.subheader("Uploader un document")
    uploaded_file = st.file_uploader("Choisir un PDF", type="pdf")
    doc_type = st.radio("Type de document", ["passager","definitif"], horizontal=True)
    tags = st.text_input("Tags (séparés par virgule)", key="tags_input")
    upload_feedback = st.empty()
    if uploaded_file and st.button("Uploader", key="upload_btn"):
        with st.spinner("Traitement du document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                data = {"doc_type": doc_type, "tags": tags}
                resp = requests.post("http://127.0.0.1:8000/upload", files=files, data=data)
                if resp.status_code == 200:
                    upload_feedback.success(resp.json().get("message", "Document traité avec succès !"))
                else:
                    upload_feedback.error(f"Erreur {resp.status_code} : {resp.text}")
            except Exception as e:
                upload_feedback.error(f"Erreur lors de l'upload : {e}")
    st.markdown("---")
    st.subheader("Historique des questions")
    try:
        hist_df = pd.read_sql(
            "SELECT * FROM questions_history ORDER BY asked_at DESC LIMIT 50",
            "postgresql://{}:{}@{}:{}/{}".format(
                os.getenv("POSTGRES_USER"),
                os.getenv("POSTGRES_PASSWORD"),
                os.getenv("POSTGRES_HOST"),
                os.getenv("POSTGRES_PORT"),
                os.getenv("POSTGRES_DB")
            )
        )
        if not hist_df.empty:
            st.dataframe(hist_df)
        else:
            st.info("Aucune question posée pour le moment.")
    except Exception as e:
        st.info(f"Impossible de récupérer l'historique : {e}")

# Main: conversation chat
st.title("🤖 Assistant Stratégique IA")
st.markdown("**Analyse de documents PDF et réponses intelligentes**")
st.header("💬 Conversation IA")

# Persistent chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

question = st.text_input("Votre question ici :", key="chat_input")
pdf_filter = st.text_input("Filtrer PDF (optionnel)", key="pdf_input")
page_filter = st.text_input("Filtrer pages (ex:2,3,4)", key="page_input")
tag_filter = st.text_input("Filtrer tags (ex:finance, contrat)", key="tag_input")

if st.button("Envoyer", key="chat_btn") and question:
    with st.spinner("Recherche et génération de réponse..."):
        try:
            data = {
                "question": question,
                "pdf_filter": pdf_filter,
                "page_filter": page_filter,
                "tag_filter": tag_filter
            }
            resp = requests.post("http://127.0.0.1:8000/chat", data=data)
            if resp.status_code == 200:
                result = resp.json()
                st.session_state["chat_history"].append({
                    "question": question,
                    "answer": result.get("answer", "Aucune réponse"),
                    "sources": result.get("sources", [])
                })
            else:
                st.error(f"Erreur {resp.status_code} : {resp.text}")
        except Exception as e:
            st.error(f"Erreur lors de la requête : {e}")

# Display chat history
for chat in st.session_state["chat_history"]:
    st.markdown(f"**Vous :** {chat['question']}")
    st.markdown(f"**Assistant :** {chat['answer']}")
    if chat["sources"]:
        st.markdown("_Sources :_")
        for src in chat["sources"]:
            st.write(f"{src.get('pdf')} → pages {src.get('pages')}")
    st.markdown("---")

# Section: Dashboard
st.header("📊 Documents stockés")
try:
    df = pd.read_sql(
        "SELECT * FROM documents",
        "postgresql://{}:{}@{}:{}/{}".format(
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_HOST"),
            os.getenv("POSTGRES_PORT"),
            os.getenv("POSTGRES_DB")
        )
    )
    st.dataframe(df)
    if not df.empty:
        fig = px.bar(
            df, 
            x="filename", 
            y=df["tags"].apply(lambda x: len(x)),
            labels={"y":"Nombre de tags"},
            color_discrete_sequence=["#0b3d91"]
        )
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.info(f"Aucun document stocké pour le moment : {e}")
