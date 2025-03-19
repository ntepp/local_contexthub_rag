# src/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag.rag_pipeline import create_and_run_graph, load_source

app = FastAPI()

class SourceLoadRequest(BaseModel):
    source: str

class QuestionRequest(BaseModel):
    question: str

@app.post("/load")
async def load_source_endpoint(request: SourceLoadRequest):
    """
    Load a document source.
    """
    try:
        load_source(request.source)
        return {"message": "Source loaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question_endpoint(request: QuestionRequest):
    """
    Ask a question about the loaded source.
    """
    try:
        answer = create_and_run_graph(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)