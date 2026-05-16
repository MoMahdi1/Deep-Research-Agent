import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = str(BASE_DIR / "data")
CHROMA_PATH = str(BASE_DIR / "data" / "chroma_db")

def load_documents(path:str) ->list:
    docs =[]
    pdf_files = list(Path(path).glob("*.pdf"))
    
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {path}")
    
    for pdf_path in pdf_files:
        print(f"[ingestion] Loading: {pdf_path.name}")
        loader = PyMuPDFLoader(str(pdf_path))
        docs.extend(loader.load())
        
    
    return docs


def split_documents(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,           
        chunk_overlap=100,       
        separators=["\n\n", "\n", "مادة", ".", " "],
    )
    chunks = splitter.split_documents(docs)
    print(f"[ingestion] Split into {len(chunks)} chunks")
    return chunks


def build_vectorstore(chunks: list) -> Chroma:
    print("[ingestion] Building embeddings — this may take a few minutes...")

    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )

    print(f"[ingestion] Vector store saved to: {CHROMA_PATH}")
    return vectorstore


def run():
    os.makedirs(DOCUMENTS_PATH, exist_ok=True)
    os.makedirs(CHROMA_PATH, exist_ok=True)

    docs   = load_documents(DOCUMENTS_PATH)
    chunks = split_documents(docs)
    build_vectorstore(chunks)


if __name__ == "__main__":
    run()
