"""
Moduł do ekstrakcji treści z dokumentów CV i ogłoszeń o pracę.
Obsługuje formaty PDF, DOCX i TXT.
"""
import os
import re
from typing import Dict, List, Optional, Tuple

import pdfplumber
from docx import Document


class DocumentParser:
    """
    Klasa do ekstrakcji treści z dokumentów w różnych formatach.
    """
    
    def __init__(self, file_path: str):
        """
        Inicjalizacja parsera dokumentów.
        
        Args:
            file_path: Ścieżka do pliku dokumentu
        """
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1].lower()
        self.content = ""
        self.sections = {}
    
    def extract_content(self) -> str:
        """
        Ekstrahuje pełną treść dokumentu.
        
        Returns:
            str: Pełna treść dokumentu
        
        Raises:
            ValueError: Jeśli format pliku nie jest obsługiwany
        """
        if self.file_extension == '.pdf':
            self.content = self._extract_from_pdf()
        elif self.file_extension == '.docx':
            self.content = self._extract_from_docx()
        elif self.file_extension == '.txt':
            self.content = self._extract_from_txt()
        else:
            raise ValueError(f"Nieobsługiwany format pliku: {self.file_extension}")
        
        return self.content
    
    def _extract_from_pdf(self) -> str:
        """
        Ekstrahuje tekst z pliku PDF.
        
        Returns:
            str: Tekst z pliku PDF
        """
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
        except Exception as e:
            raise Exception(f"Błąd podczas ekstrakcji tekstu z PDF: {str(e)}")
        
        return text
    
    def _extract_from_docx(self) -> str:
        """
        Ekstrahuje tekst z pliku DOCX.
        
        Returns:
            str: Tekst z pliku DOCX
        """
        text = ""
        try:
            doc = Document(self.file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Błąd podczas ekstrakcji tekstu z DOCX: {str(e)}")
        
        return text
    
    def _extract_from_txt(self) -> str:
        """
        Ekstrahuje tekst z pliku TXT.
        
        Returns:
            str: Tekst z pliku TXT
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Próba odczytu z innym kodowaniem, jeśli UTF-8 zawiedzie
            try:
                with open(self.file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"Błąd podczas ekstrakcji tekstu z TXT: {str(e)}")
        except Exception as e:
            raise Exception(f"Błąd podczas ekstrakcji tekstu z TXT: {str(e)}")


class CVParser(DocumentParser):
    """
    Klasa do ekstrakcji treści z dokumentów CV.
    Dziedziczy po DocumentParser i dodaje funkcje specyficzne dla CV.
    """
    
    def __init__(self, file_path: str):
        """
        Inicjalizacja parsera CV.
        
        Args:
            file_path: Ścieżka do pliku CV
        """
        super().__init__(file_path)
        self.contact_info = {}
        self.skills = []
        self.experience = []
        self.education = []
    
    def parse_cv(self) -> Dict:
        """
        Parsuje dokument CV i ekstrahuje kluczowe sekcje.
        
        Returns:
            Dict: Słownik zawierający wyodrębnione sekcje CV
        """
        # Najpierw ekstrahujemy pełną treść
        self.extract_content()
        
        # Następnie identyfikujemy i ekstrahujemy poszczególne sekcje
        self._extract_contact_info()
        self._extract_skills()
        self._extract_experience()
        self._extract_education()
        
        return {
            "contact_info": self.contact_info,
            "skills": self.skills,
            "experience": self.experience,
            "education": self.education,
            "full_text": self.content
        }
    
    def _extract_contact_info(self):
        """
        Ekstrahuje informacje kontaktowe z CV.
        """
        # Wzorce regex do wyodrębnienia informacji kontaktowych
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+\d{1,3}[- ]?)?\d{3}[- ]?\d{3}[- ]?\d{3}\b'
        
        # Wyszukiwanie emaila
        email_match = re.search(email_pattern, self.content)
        if email_match:
            self.contact_info['email'] = email_match.group(0)
        
        # Wyszukiwanie numeru telefonu
        phone_match = re.search(phone_pattern, self.content)
        if phone_match:
            self.contact_info['phone'] = phone_match.group(0)
        
        # Próba wyodrębnienia imienia i nazwiska (uproszczona metoda)
        # W rzeczywistej aplikacji należałoby użyć bardziej zaawansowanych technik NLP
        first_lines = self.content.split('\n')[:5]  # Pierwsze 5 linii
        for line in first_lines:
            line = line.strip()
            if line and len(line.split()) <= 4 and not re.search(r'@|\d', line):
                self.contact_info['name'] = line
                break
    
    def _extract_skills(self):
        """
        Ekstrahuje umiejętności z CV.
        """
        # Identyfikacja sekcji umiejętności
        skill_section_patterns = [
            r'(?i)umiejętności|skills|kompetencje|technologie|languages|języki|narzędzia|tools'
        ]
        
        # Próba znalezienia sekcji umiejętności
        skill_section = None
        for pattern in skill_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n|\Z)", self.content, re.DOTALL)
            if match:
                skill_section = match.group(3)
                break
        
        if skill_section:
            # Wyodrębnienie umiejętności z sekcji
            # Zakładamy, że umiejętności są oddzielone przecinkami, średnikami lub nowymi liniami
            skills_raw = re.split(r'[,;•\n]', skill_section)
            self.skills = [skill.strip() for skill in skills_raw if skill.strip()]
        else:
            # Jeśli nie znaleziono dedykowanej sekcji, próbujemy wyodrębnić popularne umiejętności
            common_skills = [
                "Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "SQL", "HTML", "CSS",
                "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring", "ASP.NET",
                "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "CI/CD", "Agile", "Scrum"
            ]
            
            for skill in common_skills:
                if re.search(r'\b' + re.escape(skill) + r'\b', self.content, re.IGNORECASE):
                    self.skills.append(skill)
    
    def _extract_experience(self):
        """
        Ekstrahuje doświadczenie zawodowe z CV.
        """
        # Identyfikacja sekcji doświadczenia
        exp_section_patterns = [
            r'(?i)doświadczenie|experience|zatrudnienie|praca|employment|career'
        ]
        
        # Próba znalezienia sekcji doświadczenia
        exp_section = None
        for pattern in exp_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n\n|\Z)", self.content, re.DOTALL)
            if match:
                exp_section = match.group(3)
                break
        
        if exp_section:
            # Podział na poszczególne pozycje (uproszczona metoda)
            # W rzeczywistej aplikacji należałoby użyć bardziej zaawansowanych technik NLP
            exp_entries = re.split(r'\n\n', exp_section)
            
            for entry in exp_entries:
                if entry.strip():
                    # Próba wyodrębnienia firmy i stanowiska
                    lines = entry.strip().split('\n')
                    if len(lines) >= 2:
                        position = lines[0].strip()
                        company = lines[1].strip()
                        
                        # Próba wyodrębnienia dat
                        date_pattern = r'\b(0?[1-9]|1[0-2])/\d{4}\s*-\s*(0?[1-9]|1[0-2])/\d{4}|\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*(obecnie|present)'
                        date_match = re.search(date_pattern, entry, re.IGNORECASE)
                        dates = date_match.group(0) if date_match else ""
                        
                        # Opis stanowiska
                        description = "\n".join(lines[2:]) if len(lines) > 2 else ""
                        
                        self.experience.append({
                            "position": position,
                            "company": company,
                            "dates": dates,
                            "description": description
                        })
    
    def _extract_education(self):
        """
        Ekstrahuje wykształcenie z CV.
        """
        # Identyfikacja sekcji wykształcenia
        edu_section_patterns = [
            r'(?i)edukacja|education|wykształcenie|studia|szkoła|university|college'
        ]
        
        # Próba znalezienia sekcji wykształcenia
        edu_section = None
        for pattern in edu_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n\n|\Z)", self.content, re.DOTALL)
            if match:
                edu_section = match.group(3)
                break
        
        if edu_section:
            # Podział na poszczególne pozycje (uproszczona metoda)
            edu_entries = re.split(r'\n\n', edu_section)
            
            for entry in edu_entries:
                if entry.strip():
                    # Próba wyodrębnienia uczelni i kierunku
                    lines = entry.strip().split('\n')
                    if len(lines) >= 2:
                        degree = lines[0].strip()
                        institution = lines[1].strip()
                        
                        # Próba wyodrębnienia dat
                        date_pattern = r'\b(0?[1-9]|1[0-2])/\d{4}\s*-\s*(0?[1-9]|1[0-2])/\d{4}|\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*(obecnie|present)'
                        date_match = re.search(date_pattern, entry, re.IGNORECASE)
                        dates = date_match.group(0) if date_match else ""
                        
                        self.education.append({
                            "degree": degree,
                            "institution": institution,
                            "dates": dates
                        })


class JobDescriptionParser(DocumentParser):
    """
    Klasa do ekstrakcji treści z ogłoszeń o pracę.
    Dziedziczy po DocumentParser i dodaje funkcje specyficzne dla ogłoszeń.
    """
    
    def __init__(self, file_path: str):
        """
        Inicjalizacja parsera ogłoszeń o pracę.
        
        Args:
            file_path: Ścieżka do pliku ogłoszenia
        """
        super().__init__(file_path)
        self.job_title = ""
        self.company = ""
        self.required_skills = []
        self.responsibilities = []
        self.qualifications = []
    
    def parse_job_description(self) -> Dict:
        """
        Parsuje ogłoszenie o pracę i ekstrahuje kluczowe sekcje.
        
        Returns:
            Dict: Słownik zawierający wyodrębnione sekcje ogłoszenia
        """
        # Najpierw ekstrahujemy pełną treść
        self.extract_content()
        
        # Następnie identyfikujemy i ekstrahujemy poszczególne sekcje
        self._extract_job_title()
        self._extract_company()
        self._extract_required_skills()
        self._extract_responsibilities()
        self._extract_qualifications()
        
        return {
            "job_title": self.job_title,
            "company": self.company,
            "required_skills": self.required_skills,
            "responsibilities": self.responsibilities,
            "qualifications": self.qualifications,
            "full_text": self.content
        }
    
    def _extract_job_title(self):
        """
        Ekstrahuje tytuł stanowiska z ogłoszenia.
        """
        # Próba wyodrębnienia tytułu stanowiska (uproszczona metoda)
        first_lines = self.content.split('\n')[:5]  # Pierwsze 5 linii
        for line in first_lines:
            line = line.strip()
            if line and len(line.split()) <= 6:
                self.job_title = line
                break
    
    def _extract_company(self):
        """
        Ekstrahuje nazwę firmy z ogłoszenia.
        """
        # Próba wyodrębnienia nazwy firmy (uproszczona metoda)
        company_patterns = [
            r'(?i)firma:?\s*([^\n]+)',
            r'(?i)company:?\s*([^\n]+)',
            r'(?i)pracodawca:?\s*([^\n]+)',
            r'(?i)employer:?\s*([^\n]+)'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, self.content)
            if match:
                self.company = match.group(1).strip()
                break
    
    def _extract_required_skills(self):
        """
        Ekstrahuje wymagane umiejętności z ogłoszenia.
        """
        # Identyfikacja sekcji wymaganych umiejętności
        skill_section_patterns = [
            r'(?i)wymagania|requirements|umiejętności|skills|kwalifikacje|qualifications',
            r'(?i)oczekujemy|we expect|we require'
        ]
        
        # Próba znalezienia sekcji umiejętności
        skill_section = None
        for pattern in skill_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n|\Z)", self.content, re.DOTALL)
            if match:
                skill_section = match.group(3)
                break
        
        if skill_section:
            # Wyodrębnienie umiejętności z sekcji
            # Zakładamy, że umiejętności są wymienione w punktach lub oddzielone nowymi liniami
            skills_raw = re.split(r'[•\-*]|\n', skill_section)
            self.required_skills = [skill.strip() for skill in skills_raw if skill.strip()]
    
    def _extract_responsibilities(self):
        """
        Ekstrahuje obowiązki z ogłoszenia.
        """
        # Identyfikacja sekcji obowiązków
        resp_section_patterns = [
            r'(?i)obowiązki|responsibilities|zadania|tasks|zakres obowiązków',
            r'(?i)będziesz odpowiedzialny za|you will be responsible for'
        ]
        
        # Próba znalezienia sekcji obowiązków
        resp_section = None
        for pattern in resp_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n|\Z)", self.content, re.DOTALL)
            if match:
                resp_section = match.group(3)
                break
        
        if resp_section:
            # Wyodrębnienie obowiązków z sekcji
            resp_raw = re.split(r'[•\-*]|\n', resp_section)
            self.responsibilities = [resp.strip() for resp in resp_raw if resp.strip()]
    
    def _extract_qualifications(self):
        """
        Ekstrahuje kwalifikacje z ogłoszenia.
        """
        # Identyfikacja sekcji kwalifikacji
        qual_section_patterns = [
            r'(?i)kwalifikacje|qualifications|wykształcenie|education',
            r'(?i)wymagane doświadczenie|required experience'
        ]
        
        # Próba znalezienia sekcji kwalifikacji
        qual_section = None
        for pattern in qual_section_patterns:
            match = re.search(f"({pattern}).*?(\n|$)(.*?)(\n\n|\Z)", self.content, re.DOTALL)
            if match:
                qual_section = match.group(3)
                break
        
        if qual_section:
            # Wyodrębnienie kwalifikacji z sekcji
            qual_raw = re.split(r'[•\-*]|\n', qual_section)
            self.qualifications = [qual.strip() for qual in qual_raw if qual.strip()]
