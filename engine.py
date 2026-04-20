from operator import itemgetter
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from utils import load_docs, split_docs
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import ChatHuggingFace

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline


import warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
file_path = "data/MedicalBook.pdf"

def downlode_hugging_face_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/msmarco-MiniLM-L6-v3')
    return embeddings

CHROMA_PATH="chroma_db"
#embeddings = downlode_hugging_face_embeddings()

def create_vectorstore(embeddings):
    if os.path.exists(CHROMA_PATH):
        print(f"--- Loading existing Vector DB from {CHROMA_PATH}... ---")
        # FIX: To LOAD, use Chroma() directly. Do NOT use .from_documents()
        return Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings
        )  
    else: 
        print("Creating a new one...")
        documents = load_docs(file_path)
        text_chunks = split_docs(documents)
        # Use .from_documents ONLY when you have new text_chunks to process
        return Chroma.from_documents(
            documents=text_chunks, 
            embedding=embeddings, 
            persist_directory=CHROMA_PATH 
        )

# vector_db=create_vectorstore()
# retriever=vector_db.as_retriever(search_kwargs={"k": 3})

def get_llm():
    # The correct ID for the 1B Instruct model
    model_path = "ibm-granite/granite-3.0-1b-a400m-instruct"
    
    device = -1 # Force CPU
    print(f"--- Loading local model: {model_path} ---")

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # We use low_cpu_mem_usage to keep the RAM footprint small
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32, 
        low_cpu_mem_usage=True,
        device_map=None 
    )
    
    gen_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256, 
        temperature=0.3,
        do_sample=True,
        return_full_text=False
    )
    
    llm = HuggingFacePipeline(pipeline=gen_pipeline)
    return ChatHuggingFace(llm=llm)


def get_llm_response(user_input, retriever, llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a medical specialist. Use the context to answer. If you don't know, say 'I don't know'."),
        ("human", "Context: {context}\n\nQuestion: {input}")
    ])
    
    chain = (
        {
            "context": itemgetter("input") | retriever,
            "input": itemgetter("input"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke({"input": user_input})

def load_system():
    """
    Orchestrates the loading of the full RAG pipeline.
    This can be called by both FastAPI and Streamlit.
    """
    print("--- Initializing Medical AI System ---")
    embeddings = downlode_hugging_face_embeddings()
    vector_db = create_vectorstore(embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    llm = get_llm()
    print("--- System Ready ---")
    return retriever, llm       

if __name__=="__main__":

    embeddings = downlode_hugging_face_embeddings()
    vector_db=create_vectorstore(embeddings)
    retriever=vector_db.as_retriever(search_kwargs={"k": 3})
    llm=get_llm()

#     print("\n -- LLM Testing -- \n")
#     while True:
#         User_query=input("User: ")
#         if User_query.lower() in ["quit","exit","q"]:
#             print("Exiting..")
#             break
#         response=get_llm_response(User_query, retriever, llm)
#         print(f"Assistant: {response}")



    
