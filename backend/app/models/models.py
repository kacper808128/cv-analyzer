"""
Moduły modeli ORM dla bazy danych PostgreSQL.
Definiuje strukturę tabel i relacje między nimi.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Analysis(Base):
    """
    Model analizy CV względem ogłoszenia o pracę.
    Przechowuje wyniki analizy oraz referencje do plików.
    """
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    cv_filename = Column(String(255), nullable=False)
    job_description_filename = Column(String(255), nullable=False)
    relevance_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacje
    cv_data = relationship("CVData", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    job_data = relationship("JobData", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    skill_matches = relationship("SkillMatch", back_populates="analysis", cascade="all, delete-orphan")
    section_scores = relationship("SectionScore", back_populates="analysis", cascade="all, delete-orphan")

class CVData(Base):
    """
    Model danych wyekstrahowanych z CV.
    """
    __tablename__ = "cv_data"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    contact_info = Column(JSON, nullable=True)
    skills = Column(JSON, nullable=True)  # Lista umiejętności
    experience = Column(JSON, nullable=True)  # Lista doświadczeń
    education = Column(JSON, nullable=True)  # Lista wykształcenia
    full_text = Column(Text, nullable=False)
    
    # Relacje
    analysis = relationship("Analysis", back_populates="cv_data")

class JobData(Base):
    """
    Model danych wyekstrahowanych z ogłoszenia o pracę.
    """
    __tablename__ = "job_data"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    job_title = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    required_skills = Column(JSON, nullable=True)  # Lista wymaganych umiejętności
    responsibilities = Column(JSON, nullable=True)  # Lista obowiązków
    qualifications = Column(JSON, nullable=True)  # Lista kwalifikacji
    full_text = Column(Text, nullable=False)
    
    # Relacje
    analysis = relationship("Analysis", back_populates="job_data")

class SkillMatch(Base):
    """
    Model dopasowania umiejętności z CV do wymagań z ogłoszenia.
    """
    __tablename__ = "skill_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    cv_skill = Column(String(255), nullable=False)
    job_skill = Column(String(255), nullable=False)
    similarity_score = Column(Float, nullable=False)  # Wartość od 0 do 1
    
    # Relacje
    analysis = relationship("Analysis", back_populates="skill_matches")

class SectionScore(Base):
    """
    Model oceny poszczególnych sekcji CV względem ogłoszenia.
    """
    __tablename__ = "section_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    section_name = Column(String(50), nullable=False)  # np. "skills", "experience", "education"
    score = Column(Float, nullable=False)  # Wartość od 0 do 1
    weight = Column(Float, nullable=False)  # Waga sekcji w ogólnej ocenie
    
    # Relacje
    analysis = relationship("Analysis", back_populates="section_scores")
