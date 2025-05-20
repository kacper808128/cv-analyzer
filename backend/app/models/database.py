"""
Moduł konfiguracji bazy danych PostgreSQL.
Zawiera funkcje do inicjalizacji połączenia i sesji.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja połączenia z bazą danych
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost/cv_analyzer"
)

# Tworzenie silnika SQLAlchemy
engine = create_engine(DATABASE_URL)

# Tworzenie sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funkcja pomocnicza do uzyskania sesji bazy danych
def get_db():
    """
    Funkcja pomocnicza do uzyskania sesji bazy danych.
    Używana jako zależność w endpointach FastAPI.
    
    Yields:
        Session: Sesja bazy danych
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
