from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from yt_qa_core import process_video_and_question

app = FastAPI()

# Allow CORS for local development (Chrome extension)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8000", "chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    video_id: str
    question: str

@app.post("/ask")
def ask_video_question(req: QueryRequest):
    answer = process_video_and_question(req.video_id, req.question)
    return {"answer": answer}