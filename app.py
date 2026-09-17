from pathlib import Path
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

def words(text):
    return set(re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()))

@app.post("/ask")
async def ask_rag(query: Query):
    knowledge_path = Path(__file__).with_name("knowledge.txt")
    sections = knowledge_path.read_text(encoding="utf-8").split("\n\n")

    question_words = words(query.question)
    best_section = max(
        sections,
        key=lambda section: len(question_words & words(section))
    )

    if not question_words & words(best_section):
        return {
            "answer": "I could not find an answer in the knowledge base."
        }

    return {"answer": best_section}