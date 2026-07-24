import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader

load_dotenv()

def ingest():
    all_documents = []

    # Load .txt files
    txt_loader = DirectoryLoader(
        "corpus/",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    txt_docs = txt_loader.load()
    print(f"Loaded {len(txt_docs)} text files")
    all_documents.extend(txt_docs)

    # Load .pdf files
    pdf_loader = DirectoryLoader(
        "corpus/",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    pdf_docs = pdf_loader.load()
    print(f"Loaded {len(pdf_docs)} PDF pages")
    all_documents.extend(pdf_docs)

    print(f"Total documents loaded: {len(all_documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(all_documents)
    print(f"Split into {len(chunks)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    print("Indexed successfully. chroma_db/ folder created.")

if __name__ == "__main__":
    ingest()