import ollama
from src.retrieve import retrieve_relevant_chunks


def generate_answer(query):
    chunks = retrieve_relevant_chunks(query)

    context = "\n\n".join([chunk.page_content for chunk in chunks])

    prompt = f"""
You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{query}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    query = input("Ask a question: ")
    answer = generate_answer(query)
    print("\nAnswer:\n")
    print(answer)
