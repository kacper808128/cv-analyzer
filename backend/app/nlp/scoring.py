"""
Moduł do analizy NLP i oceny relewantności CV względem ogłoszenia o pracę.
"""
from typing import Dict, List, Tuple
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class RelevanceAnalyzer:
    """
    Klasa do analizy relewantności CV względem ogłoszenia o pracę.
    Wykorzystuje modele NLP do obliczania podobieństwa semantycznego.
    """
    
    def __init__(self, model_name: str = "distiluse-base-multilingual-cased-v1"):
        """
        Inicjalizacja analizatora relewantności.
        
        Args:
            model_name: Nazwa modelu SentenceTransformer do wykorzystania
        """
        self.model = SentenceTransformer(model_name)
        self.tfidf_vectorizer = TfidfVectorizer(
            min_df=1, 
            stop_words=['i', 'oraz', 'w', 'na', 'z', 'do', 'dla', 'a', 'o', 'przez']
        )
        self.section_weights = {
            "skills": 0.5,
            "experience": 0.3,
            "education": 0.2
        }
    
    def analyze_relevance(self, cv_data: Dict, job_data: Dict) -> Dict:
        """
        Analizuje relewantność CV względem ogłoszenia o pracę.
        
        Args:
            cv_data: Dane z CV
            job_data: Dane z ogłoszenia o pracę
            
        Returns:
            Dict: Wyniki analizy relewantności
        """
        # Analiza umiejętności
        skills_score, skill_matches = self._analyze_skills(
            cv_data.get("skills", []),
            job_data.get("required_skills", [])
        )
        
        # Analiza doświadczenia
        experience_score = self._analyze_experience(
            cv_data.get("experience", []),
            job_data.get("responsibilities", []),
            job_data.get("qualifications", [])
        )
        
        # Analiza wykształcenia
        education_score = self._analyze_education(
            cv_data.get("education", []),
            job_data.get("qualifications", [])
        )
        
        # Analiza pełnego tekstu
        full_text_score = self._analyze_full_text(
            cv_data.get("full_text", ""),
            job_data.get("full_text", "")
        )
        
        # Obliczanie końcowego wyniku
        section_scores = {
            "skills": skills_score,
            "experience": experience_score,
            "education": education_score,
            "full_text": full_text_score
        }
        
        # Obliczanie ważonego wyniku
        weighted_score = (
            skills_score * self.section_weights["skills"] +
            experience_score * self.section_weights["experience"] +
            education_score * self.section_weights["education"]
        )
        
        # Przygotowanie wyniku
        result = {
            "relevance_score": round(weighted_score, 2),
            "section_scores": section_scores,
            "skill_matches": skill_matches,
            "highlighted_keywords": self._extract_highlighted_keywords(cv_data.get("full_text", ""), job_data.get("full_text", ""))
        }
        
        return result
    
    def _analyze_skills(self, cv_skills: List[str], job_skills: List[str]) -> Tuple[float, List[Dict]]:
        """
        Analizuje dopasowanie umiejętności z CV do wymagań z ogłoszenia.
        
        Args:
            cv_skills: Lista umiejętności z CV
            job_skills: Lista wymaganych umiejętności z ogłoszenia
            
        Returns:
            Tuple[float, List[Dict]]: Wynik dopasowania umiejętności i lista dopasowań
        """
        if not cv_skills or not job_skills:
            return 0.0, []
        
        # Normalizacja umiejętności (lowercase)
        cv_skills_norm = [skill.lower() for skill in cv_skills]
        job_skills_norm = [skill.lower() for skill in job_skills]
        
        # Obliczanie embeddings dla wszystkich umiejętności
        all_skills = cv_skills_norm + job_skills_norm
        embeddings = self.model.encode(all_skills)
        
        cv_embeddings = embeddings[:len(cv_skills_norm)]
        job_embeddings = embeddings[len(cv_skills_norm):]
        
        # Obliczanie macierzy podobieństwa
        similarity_matrix = cosine_similarity(cv_embeddings, job_embeddings)
        
        # Znajdowanie najlepszych dopasowań
        skill_matches = []
        matched_job_skills = set()
        total_similarity = 0.0
        
        for i, cv_skill in enumerate(cv_skills):
            best_match_idx = np.argmax(similarity_matrix[i])
            best_match_score = similarity_matrix[i][best_match_idx]
            
            if best_match_score > 0.7:  # Próg podobieństwa
                job_skill = job_skills[best_match_idx]
                skill_matches.append({
                    "cv_skill": cv_skill,
                    "job_skill": job_skill,
                    "similarity_score": float(best_match_score)
                })
                matched_job_skills.add(best_match_idx)
                total_similarity += best_match_score
        
        # Obliczanie wyniku dopasowania umiejętności
        if skill_matches:
            # Średnie podobieństwo dopasowanych umiejętności
            avg_similarity = total_similarity / len(skill_matches)
            # Pokrycie wymaganych umiejętności
            coverage = len(matched_job_skills) / len(job_skills)
            # Końcowy wynik jako średnia z podobieństwa i pokrycia
            skills_score = (avg_similarity + coverage) / 2
        else:
            skills_score = 0.0
        
        return skills_score, skill_matches
    
    def _analyze_experience(self, cv_experience: List[Dict], job_responsibilities: List[str], job_qualifications: List[str]) -> float:
        """
        Analizuje dopasowanie doświadczenia z CV do wymagań z ogłoszenia.
        
        Args:
            cv_experience: Lista doświadczeń z CV
            job_responsibilities: Lista obowiązków z ogłoszenia
            job_qualifications: Lista kwalifikacji z ogłoszenia
            
        Returns:
            float: Wynik dopasowania doświadczenia
        """
        if not cv_experience or (not job_responsibilities and not job_qualifications):
            return 0.0
        
        # Ekstrakcja opisów doświadczenia z CV
        cv_exp_descriptions = []
        for exp in cv_experience:
            description = exp.get("description", "")
            position = exp.get("position", "")
            company = exp.get("company", "")
            cv_exp_descriptions.append(f"{position} {company} {description}")
        
        # Połączenie obowiązków i kwalifikacji z ogłoszenia
        job_requirements = job_responsibilities + job_qualifications
        
        # Jeśli brak danych, zwróć 0
        if not cv_exp_descriptions or not job_requirements:
            return 0.0
        
        # Obliczanie embeddings
        cv_exp_text = " ".join(cv_exp_descriptions)
        job_req_text = " ".join(job_requirements)
        
        embeddings = self.model.encode([cv_exp_text, job_req_text])
        
        # Obliczanie podobieństwa cosinusowego
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return float(similarity)
    
    def _analyze_education(self, cv_education: List[Dict], job_qualifications: List[str]) -> float:
        """
        Analizuje dopasowanie wykształcenia z CV do wymagań z ogłoszenia.
        
        Args:
            cv_education: Lista wykształcenia z CV
            job_qualifications: Lista kwalifikacji z ogłoszenia
            
        Returns:
            float: Wynik dopasowania wykształcenia
        """
        if not cv_education or not job_qualifications:
            return 0.0
        
        # Ekstrakcja informacji o wykształceniu z CV
        cv_edu_text = []
        for edu in cv_education:
            degree = edu.get("degree", "")
            institution = edu.get("institution", "")
            cv_edu_text.append(f"{degree} {institution}")
        
        # Jeśli brak danych, zwróć 0
        if not cv_edu_text:
            return 0.0
        
        # Obliczanie embeddings
        cv_edu_text_combined = " ".join(cv_edu_text)
        job_qual_text = " ".join(job_qualifications)
        
        embeddings = self.model.encode([cv_edu_text_combined, job_qual_text])
        
        # Obliczanie podobieństwa cosinusowego
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return float(similarity)
    
    def _analyze_full_text(self, cv_text: str, job_text: str) -> float:
        """
        Analizuje podobieństwo pełnego tekstu CV i ogłoszenia.
        
        Args:
            cv_text: Pełny tekst CV
            job_text: Pełny tekst ogłoszenia
            
        Returns:
            float: Wynik podobieństwa tekstów
        """
        if not cv_text or not job_text:
            return 0.0
        
        # Obliczanie TF-IDF
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([cv_text, job_text])
        
        # Obliczanie podobieństwa cosinusowego
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    
    def _extract_highlighted_keywords(self, cv_text: str, job_text: str) -> List[str]:
        """
        Ekstrahuje słowa kluczowe z ogłoszenia, które występują w CV.
        
        Args:
            cv_text: Pełny tekst CV
            job_text: Pełny tekst ogłoszenia
            
        Returns:
            List[str]: Lista słów kluczowych do podświetlenia
        """
        if not cv_text or not job_text:
            return []
        
        # Tokenizacja tekstów
        cv_tokens = set(re.findall(r'\b\w+\b', cv_text.lower()))
        job_tokens = set(re.findall(r'\b\w+\b', job_text.lower()))
        
        # Usunięcie stop words
        stop_words = {'i', 'oraz', 'w', 'na', 'z', 'do', 'dla', 'a', 'o', 'przez', 'się', 'jest', 'są', 'być', 'to', 'że'}
        cv_tokens = cv_tokens - stop_words
        job_tokens = job_tokens - stop_words
        
        # Znalezienie wspólnych słów
        common_tokens = cv_tokens.intersection(job_tokens)
        
        # Filtrowanie słów krótszych niż 3 znaki
        highlighted_keywords = [token for token in common_tokens if len(token) > 2]
        
        return highlighted_keywords
