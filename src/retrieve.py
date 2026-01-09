from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def retrieve_relevant_chunks(query, k=3):
    # Load the same embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load FAISS vector store
    vectorstore = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True)

    # Perform similarity search
    results = vectorstore.similarity_search(query, k=k)

    return results


if __name__ == "__main__":
    query = input("Enter your question: ")
    chunks = retrieve_relevant_chunks(query)

    print("\nTop relevant chunks:\n")
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}:")
        print(chunk.page_content)
        print("-" * 50)
