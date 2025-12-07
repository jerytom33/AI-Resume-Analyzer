from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import shutil
import uuid
from resume_analyser_utils import analyze_resume

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

# Allow all CORS for Flutter app development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "Uploaded_Resumes_API"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "AI Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Generate unique filename to avoid conflicts
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Analyze resume using utility function
        result = analyze_resume(file_path)
        
        if not result:
             raise HTTPException(status_code=500, detail="Failed to parse resume")

        # Clean up file after analysis (optional, keeping for debugging or future requirements)
        # os.remove(file_path) 

        return {
            "status": "success",
            "filename": file.filename,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
