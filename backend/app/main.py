"""
Główny moduł aplikacji FastAPI do analizy CV.
Zawiera konfigurację aplikacji oraz główne endpointy API.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
import uuid
from datetime import datetime

# Utworzenie instancji aplikacji FastAPI
app = FastAPI(
    title="CV Analyzer API",
    description="API do analizy CV pod kątem zgodności z treścią ogłoszenia o pracę",
    version="0.1.0"
)

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W środowisku produkcyjnym należy ograniczyć do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utworzenie katalogu na przesłane pliki
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Dozwolone rozszerzenia plików
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

def validate_file_extension(filename: str) -> bool:
    """
    Sprawdza, czy rozszerzenie pliku jest dozwolone.
    
    Args:
        filename: Nazwa pliku do sprawdzenia
        
    Returns:
        bool: True jeśli rozszerzenie jest dozwolone, False w przeciwnym przypadku
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/health")
async def health_check():
    """
    Endpoint do sprawdzenia statusu aplikacji.
    
    Returns:
        dict: Status aplikacji
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.post("/analyze")
async def analyze_cv(
    cv_file: UploadFile = File(...),
    job_description_file: UploadFile = File(...),
):
    """
    Endpoint do analizy CV pod kątem zgodności z treścią ogłoszenia o pracę.
    
    Args:
        cv_file: Plik CV w formacie PDF, DOCX lub TXT
        job_description_file: Plik z ogłoszeniem o pracę w formacie PDF, DOCX lub TXT
        
    Returns:
        dict: Wyniki analizy CV
        
    Raises:
        HTTPException: Jeśli pliki mają nieprawidłowe rozszerzenia lub wystąpił błąd podczas przetwarzania
    """
    # Walidacja rozszerzeń plików
    if not validate_file_extension(cv_file.filename):
        raise HTTPException(status_code=400, detail="Nieprawidłowy format pliku CV. Dozwolone formaty: PDF, DOCX, TXT")
    
    if not validate_file_extension(job_description_file.filename):
        raise HTTPException(status_code=400, detail="Nieprawidłowy format pliku ogłoszenia. Dozwolone formaty: PDF, DOCX, TXT")
    
    # Generowanie unikalnych nazw plików
    cv_filename = f"{uuid.uuid4()}_{cv_file.filename}"
    job_desc_filename = f"{uuid.uuid4()}_{job_description_file.filename}"
    
    # Zapisywanie plików
    cv_path = os.path.join(UPLOAD_DIR, cv_filename)
    job_desc_path = os.path.join(UPLOAD_DIR, job_desc_filename)
    
    try:
        # Zapisanie plików na dysku
        with open(cv_path, "wb") as f:
            shutil.copyfileobj(cv_file.file, f)
        
        with open(job_desc_path, "wb") as f:
            shutil.copyfileobj(job_description_file.file, f)
            
        # TODO: Implementacja ekstrakcji treści i analizy NLP
        
        # Tymczasowa odpowiedź (do zastąpienia rzeczywistą analizą)
        return {
            "status": "success",
            "message": "Pliki zostały przesłane pomyślnie",
            "files": {
                "cv": cv_filename,
                "job_description": job_desc_filename
            },
            "analysis": {
                "relevance_score": 0.0,  # Placeholder
                "skills_match": [],      # Placeholder
                "experience_match": [],  # Placeholder
                "education_match": []    # Placeholder
            }
        }
    
    except Exception as e:
        # Usunięcie plików w przypadku błędu
        if os.path.exists(cv_path):
            os.remove(cv_path)
        if os.path.exists(job_desc_path):
            os.remove(job_desc_path)
        
        raise HTTPException(status_code=500, detail=f"Wystąpił błąd podczas przetwarzania plików: {str(e)}")
    finally:
        # Zamknięcie plików
        cv_file.file.close()
        job_description_file.file.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
