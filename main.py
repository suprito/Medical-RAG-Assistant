from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from engine import load_system, get_llm_response


app=FastAPI(
    title="Medical RAG API",
    description="Backend API for IBM Granite chat model",
    version="1.0.0")

#gloabal model loading 
print("Loading Medical AI Engine... Please wait.")
retriever, llm = load_system()
print("AI loaded successfully.")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"status":"online","message": "Medical API is Ready"}

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    try:
        # Using the globally loaded retriever and llm
        response = get_llm_response(request.query, retriever, llm)
        return ChatResponse(answer=response)
    except Exception as e:
        # Standard API error handling
        raise HTTPException(status_code=500, detail=str(e))