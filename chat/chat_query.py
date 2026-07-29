import os 
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import asyncio

load_dotenv()

llm = ChatOpenAI(model='gpt-4o')

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    persist_directory='./chroma_db',
    embedding_function=embedding_model
)

prompt = PromptTemplate(
    template="""
    You are the helpful assistant. Answer the following question
    based only on the provided conotext
    Question: {question}
    content{context}
    Include the document sources if relevent in your answer.
    """
)

chain = prompt | llm

async def answer_query(query:str,user_role:str):
    docs = await asyncio.to_thread(
        vectorstore.similarity_search,
        query,
        k=3
    )

    filtered_context = []
    sources = set()

    for doc in docs:
        metadata = doc.metadata

        if metadata.get("role") == user_role:
            filtered_context.append(doc.page_content)
            sources.add(metadata.get("source"))

    if not filtered_context:
        {"message":"No relevent info found"}

    docs_text = "\n".join(filtered_context)

    final_answer = await asyncio.to_thread(
        chain.invoke,
        {
            "question":query,
            "context":docs_text
        }
    )

    return {
        "Answer":final_answer.content,
        "Sources":list(sources)
    }

