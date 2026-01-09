from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import shutil
import os
from fastapi import Form


from src.ingest import ingest_documents
from src.generate import generate_answer

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>RAG Document Assistant</h1>

            <h3>Upload PDF</h3>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit">
            </form>

            <h3>Ask Question</h3>
            <form action="/ask" method="post">
                <input type="text" name="question" style="width:300px">
                <input type="submit">
            </form>
        </body>
    </html>
    """


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"data/docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_documents(file_path)

    return {"message": "File uploaded and processed successfully"}


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    answer = generate_answer(question)
    return {"answer": answer}
