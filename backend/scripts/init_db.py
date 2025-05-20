"""
Skrypt do inicjalizacji bazy danych i wstawiania przykładowych danych.
"""
import os
import sys
import json
from datetime import datetime

# Dodanie ścieżki do katalogu głównego projektu
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.models import Base, Analysis, CVData, JobData, SkillMatch, SectionScore
from app.models.database import engine, SessionLocal

def create_tables():
    """
    Tworzy tabele w bazie danych na podstawie modeli ORM.
    """
    Base.metadata.create_all(bind=engine)
    print("Tabele zostały utworzone.")

def insert_sample_data():
    """
    Wstawia przykładowe dane do bazy danych.
    """
    db = SessionLocal()
    try:
        # Tworzenie przykładowej analizy
        analysis = Analysis(
            cv_filename="przyklad_cv.pdf",
            job_description_filename="przyklad_ogloszenie.pdf",
            relevance_score=0.75,
            created_at=datetime.now()
        )
        db.add(analysis)
        db.flush()  # Aby uzyskać ID analizy
        
        # Dane CV
        cv_data = CVData(
            analysis_id=analysis.id,
            contact_info=json.dumps({
                "name": "Jan Kowalski",
                "email": "jan.kowalski@example.com",
                "phone": "+48 123 456 789"
            }),
            skills=json.dumps([
                "Python", "JavaScript", "React", "Node.js", "SQL", "Docker", 
                "Git", "REST API", "TypeScript", "FastAPI"
            ]),
            experience=json.dumps([
                {
                    "position": "Senior Full-Stack Developer",
                    "company": "Tech Solutions Sp. z o.o.",
                    "dates": "2020 - obecnie",
                    "description": "Rozwój aplikacji webowych z wykorzystaniem React i Node.js."
                },
                {
                    "position": "Full-Stack Developer",
                    "company": "WebDev Company",
                    "dates": "2018 - 2020",
                    "description": "Implementacja funkcjonalności front-end i back-end."
                }
            ]),
            education=json.dumps([
                {
                    "degree": "Magister Informatyki",
                    "institution": "Politechnika Warszawska",
                    "dates": "2016 - 2018"
                },
                {
                    "degree": "Inżynier Informatyki",
                    "institution": "Politechnika Warszawska",
                    "dates": "2012 - 2016"
                }
            ]),
            full_text="Jan Kowalski\nSenior Full-Stack Developer\n\nKontakt:\nEmail: jan.kowalski@example.com\nTelefon: +48 123 456 789\n\nDoświadczenie:\nSenior Full-Stack Developer\nTech Solutions Sp. z o.o.\n2020 - obecnie\nRozwój aplikacji webowych z wykorzystaniem React i Node.js.\n\nFull-Stack Developer\nWebDev Company\n2018 - 2020\nImplementacja funkcjonalności front-end i back-end.\n\nWykształcenie:\nMagister Informatyki\nPolitechnika Warszawska\n2016 - 2018\n\nInżynier Informatyki\nPolitechnika Warszawska\n2012 - 2016\n\nUmiejętności:\nPython, JavaScript, React, Node.js, SQL, Docker, Git, REST API, TypeScript, FastAPI"
        )
        db.add(cv_data)
        
        # Dane ogłoszenia o pracę
        job_data = JobData(
            analysis_id=analysis.id,
            job_title="Senior Full-Stack Developer",
            company="Innowacyjne Rozwiązania IT",
            required_skills=json.dumps([
                "JavaScript", "TypeScript", "React", "Node.js", "Python", 
                "SQL", "NoSQL", "Docker", "Kubernetes", "CI/CD"
            ]),
            responsibilities=json.dumps([
                "Rozwój aplikacji webowych",
                "Implementacja nowych funkcjonalności",
                "Optymalizacja wydajności",
                "Code review",
                "Współpraca z zespołem UX/UI"
            ]),
            qualifications=json.dumps([
                "Min. 3 lata doświadczenia w rozwoju aplikacji webowych",
                "Znajomość React i Node.js",
                "Doświadczenie z bazami danych SQL i NoSQL",
                "Znajomość konteneryzacji (Docker)",
                "Wykształcenie wyższe techniczne"
            ]),
            full_text="Senior Full-Stack Developer\nInnowacyjne Rozwiązania IT\n\nO firmie:\nInnowacyjne Rozwiązania IT to dynamicznie rozwijająca się firma z branży IT.\n\nObowiązki:\n- Rozwój aplikacji webowych\n- Implementacja nowych funkcjonalności\n- Optymalizacja wydajności\n- Code review\n- Współpraca z zespołem UX/UI\n\nWymagania:\n- Min. 3 lata doświadczenia w rozwoju aplikacji webowych\n- Znajomość React i Node.js\n- Doświadczenie z bazami danych SQL i NoSQL\n- Znajomość konteneryzacji (Docker)\n- Wykształcenie wyższe techniczne\n\nUmiejętności:\n- JavaScript\n- TypeScript\n- React\n- Node.js\n- Python\n- SQL\n- NoSQL\n- Docker\n- Kubernetes\n- CI/CD"
        )
        db.add(job_data)
        
        # Dopasowania umiejętności
        skill_matches = [
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="JavaScript",
                job_skill="JavaScript",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="TypeScript",
                job_skill="TypeScript",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="React",
                job_skill="React",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="Node.js",
                job_skill="Node.js",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="Python",
                job_skill="Python",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="SQL",
                job_skill="SQL",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="Docker",
                job_skill="Docker",
                similarity_score=1.0
            ),
            SkillMatch(
                analysis_id=analysis.id,
                cv_skill="Git",
                job_skill="CI/CD",
                similarity_score=0.6
            )
        ]
        for match in skill_matches:
            db.add(match)
        
        # Oceny sekcji
        section_scores = [
            SectionScore(
                analysis_id=analysis.id,
                section_name="skills",
                score=0.8,
                weight=0.5
            ),
            SectionScore(
                analysis_id=analysis.id,
                section_name="experience",
                score=0.7,
                weight=0.3
            ),
            SectionScore(
                analysis_id=analysis.id,
                section_name="education",
                score=0.6,
                weight=0.2
            )
        ]
        for score in section_scores:
            db.add(score)
        
        db.commit()
        print("Przykładowe dane zostały wstawione do bazy danych.")
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas wstawiania danych: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
