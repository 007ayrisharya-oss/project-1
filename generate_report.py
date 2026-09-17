from pathlib import Path
import textwrap


OUTPUT = Path(__file__).with_name("RAG_Document_Assistant_Project_Report.pdf")

REPORT = [
    ("title", "RAG Document Assistant"),
    ("subtitle", "Project Report"),
    ("paragraph", "A local, web-based document question-answering application built with HTML, JavaScript, Python, and FastAPI."),
    ("heading", "1. Executive Summary"),
    ("paragraph", "This project implements a basic Retrieval-Augmented Generation (RAG)-style document assistant. Users ask questions through a browser chat interface. A FastAPI backend reads a local knowledge base, retrieves the most relevant paragraph using keyword overlap, and returns that evidence to the user."),
    ("paragraph", "The application demonstrates the full frontend-to-backend AI application flow: user input, API communication, document retrieval, answer delivery, error handling, and a responsive chat experience."),
    ("heading", "2. Problem Statement"),
    ("paragraph", "Teams often spend time searching policy documents, procedures, and operational notes for simple answers. This project provides a lightweight assistant that can retrieve relevant information from a maintained knowledge base."),
    ("heading", "3. Objectives"),
    ("bullet", "Build a browser-based chat interface for questions about internal documents."),
    ("bullet", "Create a FastAPI endpoint to receive and process questions."),
    ("bullet", "Retrieve the most relevant section from a local knowledge base."),
    ("bullet", "Return a clear fallback response when no relevant information is found."),
    ("bullet", "Add practical UI features such as Enter-to-send, a loading state, scrolling, and error handling."),
    ("heading", "4. Technology Stack"),
    ("bullet", "Frontend: HTML, CSS, and vanilla JavaScript."),
    ("bullet", "Backend: Python, FastAPI, Uvicorn, and Pydantic."),
    ("bullet", "Knowledge base: Plain-text file (knowledge.txt)."),
    ("bullet", "Development environment: VS Code and Live Server."),
    ("heading", "5. System Architecture"),
    ("paragraph", "User -> index.html -> POST /ask -> FastAPI app.py -> knowledge.txt -> relevant paragraph -> JSON response -> browser chat."),
    ("heading", "6. Implementation Details"),
    ("heading", "6.1 Frontend - index.html"),
    ("paragraph", "The page contains a question input, Send button, and chat box. The sendMessage function takes the question, displays it, and uses fetch to send a JSON POST request to http://127.0.0.1:8000/ask. The returned answer is shown in the chat."),
    ("paragraph", "The addMessage helper creates DOM elements using textContent and createTextNode rather than inserting user text as HTML. This is safer because typed text is displayed as text, not executable markup."),
    ("bullet", "Enter key support sends the question without clicking Send."),
    ("bullet", "Thinking status gives the user feedback while a request is running."),
    ("bullet", "The input and button are disabled during the request to prevent duplicates."),
    ("bullet", "Automatic scrolling keeps the newest message visible."),
    ("bullet", "Error handling reports when the local backend is unavailable."),
    ("heading", "6.2 Backend - app.py"),
    ("paragraph", "FastAPI exposes a POST endpoint named /ask. Pydantic validates that every request contains a question string. CORS middleware allows the browser page and local backend to communicate while they run on different ports."),
    ("paragraph", "The backend reads knowledge.txt and splits it into sections at blank lines. Each paragraph is therefore treated as one retrieval chunk."),
    ("heading", "6.3 Retrieval Logic"),
    ("paragraph", "The words function converts text to lowercase and extracts alphabetic words of three or more letters. For every paragraph, the application counts the words shared with the user's question. The paragraph with the highest count is selected."),
    ("paragraph", "For example, a question containing 'maintenance' matches the paragraph 'System maintenance occurs every Sunday at midnight UTC.' If no words overlap, the app returns: I could not find an answer in the knowledge base."),
    ("heading", "7. RAG Explanation"),
    ("paragraph", "RAG stands for Retrieval-Augmented Generation. A production RAG system retrieves relevant source text and passes it to a language model, which then writes a grounded answer. This project implements the retrieval foundation and returns the retrieved evidence directly. It does not yet use embeddings, a vector database, or an LLM."),
    ("heading", "8. How to Run the Project"),
    ("bullet", "Install dependencies: python -m pip install fastapi uvicorn"),
    ("bullet", "Start the backend: python -m uvicorn app:app --reload"),
    ("bullet", "Open index.html with Live Server."),
    ("bullet", "Ask a question that contains terms found in knowledge.txt."),
    ("heading", "9. Current Limitations"),
    ("bullet", "Retrieval depends on exact keyword overlap; it does not understand semantic similarity."),
    ("bullet", "Only plain-text knowledge is supported."),
    ("bullet", "The system returns source text rather than an LLM-generated answer."),
    ("bullet", "The local CORS configuration allows all origins and should be restricted before deployment."),
    ("heading", "10. Future Enhancements"),
    ("bullet", "Use embeddings and ChromaDB or FAISS for semantic search."),
    ("bullet", "Support PDF, CSV, and document uploads."),
    ("bullet", "Use an LLM to generate concise answers only from retrieved context."),
    ("bullet", "Add source citations, confidence scores, authentication, and a SQLite audit log."),
    ("bullet", "Extend the solution into an operations exception-resolution copilot for policies, invoices, and SOPs."),
    ("heading", "11. Conclusion"),
    ("paragraph", "The RAG Document Assistant successfully proves an end-to-end AI application workflow. It provides a strong foundation for a more advanced enterprise knowledge assistant because its components are modular: the interface, API, retrieval logic, and knowledge base can each be upgraded independently."),
]


def escape_pdf(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_lines():
    lines = []
    for kind, value in REPORT:
        if kind == "title":
            lines.extend([("title", value), ("space", "")])
        elif kind == "subtitle":
            lines.extend([("subtitle", value), ("space", "")])
        elif kind == "heading":
            lines.extend([("space", ""), ("heading", value)])
        elif kind == "bullet":
            lines.extend(("body", "- " + part) for part in textwrap.wrap(value, width=88, subsequent_indent="  "))
        else:
            lines.extend(("body", part) for part in textwrap.wrap(value, width=92))
            lines.append(("space", ""))
    return lines


def content_stream(page_lines, page_number, total_pages):
    commands = ["BT", "/F1 10 Tf", "50 770 Td", "14 TL"]
    for kind, value in page_lines:
        if kind == "title":
            commands.extend(["/F2 22 Tf", f"({escape_pdf(value)}) Tj", "/F1 10 Tf", "T*"])
        elif kind == "subtitle":
            commands.extend(["/F2 14 Tf", f"({escape_pdf(value)}) Tj", "/F1 10 Tf", "T*"])
        elif kind == "heading":
            commands.extend(["/F2 13 Tf", f"({escape_pdf(value)}) Tj", "/F1 10 Tf", "T*"])
        elif kind == "space":
            commands.append("T*")
        else:
            commands.extend([f"({escape_pdf(value)}) Tj", "T*"])
    commands.extend(["ET", "BT", "/F1 8 Tf", "50 30 Td", f"(RAG Document Assistant Project Report | Page {page_number} of {total_pages}) Tj", "ET"])
    return "\n".join(commands)


def build_pdf():
    per_page = 45
    lines = make_lines()
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)]
    objects = ["<< /Type /Catalog /Pages 2 0 R >>", ""]
    page_ids, content_ids = [], []
    next_id = 5
    for _ in pages:
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2
    objects[1] = "<< /Type /Pages /Kids [" + " ".join(f"{pid} 0 R" for pid in page_ids) + f"] /Count {len(pages)} >>"
    objects.extend(["<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"])
    for index, page in enumerate(pages):
        stream = content_stream(page, index + 1, len(pages))
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {content_ids[index]} 0 R >>")
        objects.append(f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream")
    payload = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{number} 0 obj\n{obj}\nendobj\n".encode("latin-1"))
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin-1"))
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    payload.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1"))
    OUTPUT.write_bytes(payload)


if __name__ == "__main__":
    build_pdf()
    print(f"Created {OUTPUT.name}")
