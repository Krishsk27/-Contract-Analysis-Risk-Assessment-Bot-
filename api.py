from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from src.document_processor import DocumentProcessor
from src.llm_engine import ContractAnalyzer
from src.report_generator import generate_pdf_report
import shutil
import os

# --- 1. INITIALIZE APP FIRST (Must be at the top) ---
app = FastAPI()

# --- 2. SETUP CORS (Allows Frontend to talk to Backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. INITIALIZE ENGINES ---
analyzer = ContractAnalyzer()

# --- 4. DEFINE ENDPOINTS ---
@app.post("/analyze")
async def analyze_contract(
    file: UploadFile = File(...), 
    language: str = Form("English")
):
    # A. Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # B. Extract Text
    text, error = DocumentProcessor.extract_text(temp_filename)
    
    # Clean up immediately
    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    # C. Handle Extraction Errors
    if error:
        return {
            "error": error, 
            "risk_score": 0, 
            "clauses": [], 
            "summary": "Could not extract text.",
            "executive_advice": "Please upload a valid text-based PDF or DOCX."
        }
    
    # D. Analyze with AI
    result = analyzer.analyze_contract(text, language=language)
    
    return result

@app.post("/generate-pdf")
async def generate_pdf(data: dict):
    # This endpoint is optional for now, but good to keep
    try:
        pdf_bytes = generate_pdf_report(data, "contract.pdf")
        return {"status": "success", "size": len(pdf_bytes)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Run using: uvicorn api:app --reload