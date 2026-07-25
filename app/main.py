from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from app.service.rag_service import rag_service




app = FastAPI(
    title="Simple RAG API Gemini & LangChain",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question:str

class IngestRequest(BaseModel):
    file_path:str

@app.post("/ingest")
def ingest_file(payload:IngestRequest):
    try:
        rag_service.ingest_document(payload.file_path)
        return {"status":"success","message":f"Document {payload.file_path} indexe avec succes !"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@app.post("/ask")
def ask_question(payload:QueryRequest):

    try:

        answer = rag_service.ask(payload.question)
        return {"question": payload.question,"answer":answer}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))