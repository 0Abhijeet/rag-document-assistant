from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import shutil


def ingest_documents(file_path):
    # Delete old vector store
    if os.path.exists("vector_store"):
        shutil.rmtree("vector_store")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("vector_store")

    print("Documents ingested and stored successfully")


if __name__ == "__main__":
    ingest_documents("data/docs/AR_CITIZEN_Paper.pdf")
