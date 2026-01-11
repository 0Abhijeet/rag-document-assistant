from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import shutil
import os

from src.ingest import ingest_documents
from src.generate import stream_answer

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>RAG Chat Assistant</title>
            <style>
                :root {
                    --bg: #f5f5f5;
                    --text: #000;
                    --box: #ffffff;
                    --user: #DCF8C6;
                    --bot: #eeeeee;
                }

                body.dark {
                    --bg: #121212;
                    --text: #ffffff;
                    --box: #1e1e1e;
                    --user: #2e7d32;
                    --bot: #2a2a2a;
                }

                body {
                    font-family: Arial, sans-serif;
                    max-width: 700px;
                    margin: auto;
                    padding: 20px;
                    background-color: var(--bg);
                    color: var(--text);
                    transition: 0.3s;
                }

                h1 {
                    text-align: center;
                }

                .box {
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    background: var(--box);
                }

                .chat-container {
                    border: 1px solid #ddd;
                    padding: 10px;
                    height: 400px;
                    overflow-y: auto;
                    border-radius: 8px;
                    background: var(--box);
                }

                .message {
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 8px;
                    max-width: 80%;
                    white-space: pre-wrap;
                }

                .user {
                    background-color: var(--user);
                    margin-left: auto;
                }

                .bot {
                    background-color: var(--bot);
                    margin-right: auto;
                }

                .input-row {
                    display: flex;
                    gap: 10px;
                }

                input[type="text"] {
                    flex: 1;
                    padding: 8px;
                }

                button {
                    padding: 8px 12px;
                    cursor: pointer;
                }

                #status {
                    margin-top: 10px;
                    color: green;
                }

                .top-bar {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
            </style>
        </head>
        <body>
            <div class="top-bar">
                <h1>📄 RAG Chat Assistant</h1>
                <button onclick="toggleTheme()">🌙</button>
            </div>

            <div class="box">
                <h3>Upload PDF</h3>
                <input type="file" id="fileInput" />
                <br><br>
                <button onclick="uploadFile()">Upload</button>
                <p id="status"></p>
            </div>

            <div class="box">
                <h3>Chat</h3>
                <div id="chat" class="chat-container"></div>
                <br>
                <div class="input-row">
                    <input type="text" id="questionInput" placeholder="Type your question..." />
                    <button onclick="askQuestion()">Send</button>
                </div>
            </div>

            <script>
                const chatBox = document.getElementById("chat");

                function toggleTheme() {
                    document.body.classList.toggle("dark");
                }

                function addMessage(text, className) {
                    const div = document.createElement("div");
                    div.className = "message " + className;
                    div.innerText = text;
                    chatBox.appendChild(div);
                    chatBox.scrollTop = chatBox.scrollHeight;
                    return div;
                }

                async function uploadFile() {
                    const fileInput = document.getElementById("fileInput");
                    const status = document.getElementById("status");

                    if (!fileInput.files.length) {
                        alert("Please select a file.");
                        return;
                    }

                    const formData = new FormData();
                    formData.append("file", fileInput.files[0]);

                    status.innerText = "Uploading and processing...";

                    const response = await fetch("/upload", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();
                    status.innerText = data.message;
                }

                async function askQuestion() {
                    const input = document.getElementById("questionInput");
                    const question = input.value;

                    if (!question) return;

                    addMessage(question, "user");
                    input.value = "";

                    const botBubble = addMessage("", "bot");

                    const response = await fetch("/stream", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        body: new URLSearchParams({ question })
                    });

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();

                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        const chunk = decoder.decode(value);
                        botBubble.innerText += chunk;
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                }
            </script>

        </body>
    </html>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("data/docs", exist_ok=True)

    file_path = f"data/docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_documents(file_path)

    return {"message": "File uploaded and processed successfully!"}

@app.post("/stream")
async def stream_endpoint(question: str = Form(...)):
    generator = stream_answer(question)
    return StreamingResponse(generator, media_type="text/plain")
