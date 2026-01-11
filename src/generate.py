import ollama
from src.retrieve import retrieve_relevant_chunks

def stream_answer(question):
    context_docs = retrieve_relevant_chunks(question)

    # Extract text from Document objects
    context_text = "\n".join([doc.page_content for doc in context_docs])

    prompt = f"""
You are a helpful assistant. Use the following context to answer the question.

Context:
{context_text}

Question: {question}
Answer:
"""

    stream = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            yield chunk["message"]["content"]
