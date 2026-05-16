from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent.parent

CHROMA_PATH = str(BASE_DIR / "data" / "chroma_db")



embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-small"
)

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 3
        
    }
)


def get_retriever():
    return retriever