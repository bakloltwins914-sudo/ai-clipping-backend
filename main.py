import os
import uuid
import time
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: Dict[str, Dict] = {}

class ProcessRequest(BaseModel):
    video_url: str
    openai_key: str
    settings: dict

def fake_ai_processing(job_id: str):
    time.sleep(5)
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["clips"] = [
        {
            "clip_url": "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
            "duration": 30,
            "viral_score": 8.7
        }
    ]

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/process")
def process_video(request: ProcessRequest):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {
        "status": "processing",
        "clips": []
    }

    thread = threading.Thread(target=fake_ai_processing, args=(job_id,))
    thread.start()

    return {"job_id": job_id}

@app.get("/status/{job_id}")
def check_status(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}

    return jobs[job_id]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
