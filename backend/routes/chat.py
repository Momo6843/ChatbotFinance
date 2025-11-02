from fastapi import APIRouter, Form
from backend.services.rag import retrieve_context, generate_answer
from backend.db.postgres import cursor, conn

router = APIRouter()

@router.post("/chat")
async def chat(
    question: str = Form(...),
    pdf_filter: str = Form(None),
    page_filter: str = Form(None),
    tag_filter: str = Form(None)
):
    pages = list(map(int, page_filter.split(","))) if page_filter else None
    tags = tag_filter.split(",") if tag_filter else None

    context_texts, context_meta = retrieve_context(question, pdf_filter, pages, tags)
    answer = generate_answer(question, context_texts)

    pdf_names = [m['pdf'] for m in context_meta]
    page_numbers = [m['pages'] for m in context_meta]
    cursor.execute(
    "INSERT INTO questions_history (question, answer, pdf_name, page_numbers) VALUES (%s, %s, %s, %s)",
    (question, answer, ",".join(pdf_names), "{" + ",".join(str(p) for p in page_numbers) + "}")
    )
    conn.commit()
    return {"answer": answer, "sources": context_meta}
