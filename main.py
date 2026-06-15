from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from backend.nlp_engine import extract_text_from_pdf, calculate_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

@app.post("/process")
async def process_resumes(job_description: str = Form(...), files: list[UploadFile] = File(...)):
    results = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        resume_text = extract_text_from_pdf(file_path)
        score = calculate_score(job_description, resume_text)
        
        results.append({"filename": file.filename, "score": score})
    
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)