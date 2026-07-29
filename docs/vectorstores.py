import os 
import time
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()


UPLOAD_DIR = './upload_dir'
os.makedirs(UPLOAD_DIR,exist_ok=True)


async def load_vectorstores(upload_files, role: str, doc_id: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )

    for file in upload_files:
        save_path = Path(UPLOAD_DIR) / file.filename

        with open(save_path, "wb") as f:
            f.write(await file.read())

        loader = PyPDFLoader(str(save_path))
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)

        for chunk in chunks:
            chunk.metadata.update({
                "role": role,
                "doc_id": doc_id,
                "source": file.filename
            })

        vectorstore.add_documents(chunks)
        print(f"Uploaded & Indexed: {file.filename}")

    vectorstore.persist()
    print("All documents stored in ChromaDB")
