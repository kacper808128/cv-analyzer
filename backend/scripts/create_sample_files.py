"""
Skrypt do tworzenia przykładowych plików CV i ogłoszeń o pracę do testów.
"""
import os

# Ścieżka do katalogu z przykładowymi danymi
SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sample_data")
os.makedirs(SAMPLE_DIR, exist_ok=True)

# Przykładowe CV
SAMPLE_CV = """Jan Kowalski
Senior Full-Stack Developer

Kontakt:
Email: jan.kowalski@example.com
Telefon: +48 123 456 789
LinkedIn: linkedin.com/in/jankowalski

Podsumowanie zawodowe:
Doświadczony Full-Stack Developer z ponad 5-letnim doświadczeniem w tworzeniu aplikacji webowych. Specjalizuję się w technologiach JavaScript/TypeScript, React, Node.js oraz Python. Posiadam umiejętność pracy w środowisku Agile i doświadczenie w prowadzeniu małych zespołów programistycznych.

Doświadczenie zawodowe:

Senior Full-Stack Developer
Tech Solutions Sp. z o.o.
2020 - obecnie
- Rozwój aplikacji webowych z wykorzystaniem React i Node.js
- Implementacja architektury mikroserwisowej
- Optymalizacja wydajności aplikacji
- Code review i mentoring juniorów
- Wdrażanie praktyk CI/CD

Full-Stack Developer
WebDev Company
2018 - 2020
- Implementacja funkcjonalności front-end i back-end
- Integracja z zewnętrznymi API
- Rozwój aplikacji mobilnych z React Native
- Utrzymanie i rozwój baz danych SQL i NoSQL

Junior Developer
StartupTech
2016 - 2018
- Rozwój interfejsów użytkownika z wykorzystaniem React
- Implementacja REST API z wykorzystaniem Express.js
- Testowanie aplikacji

Wykształcenie:

Magister Informatyki
Politechnika Warszawska
2016 - 2018

Inżynier Informatyki
Politechnika Warszawska
2012 - 2016

Umiejętności techniczne:
- Języki programowania: JavaScript, TypeScript, Python, HTML, CSS
- Frontend: React, Redux, Angular, Vue.js
- Backend: Node.js, Express, FastAPI, Django
- Bazy danych: PostgreSQL, MongoDB, Redis
- DevOps: Docker, Kubernetes, AWS, CI/CD
- Narzędzia: Git, Jira, Confluence, Webpack
- Metodologie: Agile, Scrum, TDD

Języki:
- Polski - ojczysty
- Angielski - biegły (C1)
- Niemiecki - podstawowy (A2)

Certyfikaty:
- AWS Certified Developer - Associate
- MongoDB Certified Developer
- Certified Scrum Master

Projekty:
- E-commerce platform - aplikacja do zarządzania sklepem internetowym
- CRM system - system do zarządzania relacjami z klientami
- Task management tool - narzędzie do zarządzania zadaniami w zespole

Zainteresowania:
- Nowe technologie
- Open source
- Sztuczna inteligencja
- Podróże
"""

# Przykładowe ogłoszenie o pracę
SAMPLE_JOB = """Senior Full-Stack Developer
Innowacyjne Rozwiązania IT

O firmie:
Innowacyjne Rozwiązania IT to dynamicznie rozwijająca się firma z branży IT, specjalizująca się w tworzeniu nowoczesnych aplikacji webowych i mobilnych dla klientów z różnych sektorów. Nasz zespół składa się z doświadczonych specjalistów, którzy cenią sobie profesjonalizm, kreatywność i innowacyjne podejście do rozwiązywania problemów.

Opis stanowiska:
Poszukujemy doświadczonego Senior Full-Stack Developera, który dołączy do naszego zespołu i weźmie udział w rozwoju zaawansowanych aplikacji webowych. Osoba na tym stanowisku będzie odpowiedzialna za projektowanie, implementację i utrzymanie aplikacji, współpracę z zespołem UX/UI oraz udział w podejmowaniu kluczowych decyzji technologicznych.

Obowiązki:
- Rozwój aplikacji webowych z wykorzystaniem nowoczesnych technologii
- Implementacja nowych funkcjonalności zarówno po stronie front-end, jak i back-end
- Optymalizacja wydajności istniejących rozwiązań
- Code review i zapewnienie wysokiej jakości kodu
- Współpraca z zespołem UX/UI przy projektowaniu interfejsów użytkownika
- Udział w planowaniu sprintów i estymacji zadań
- Mentoring dla mniej doświadczonych członków zespołu

Wymagania:
- Minimum 3 lata doświadczenia w rozwoju aplikacji webowych
- Bardzo dobra znajomość JavaScript/TypeScript, React i Node.js
- Doświadczenie z bazami danych SQL (PostgreSQL) i NoSQL (MongoDB)
- Znajomość konteneryzacji (Docker) i orkiestracji (Kubernetes)
- Doświadczenie w pracy z systemami kontroli wersji (Git)
- Znajomość praktyk CI/CD
- Umiejętność pracy w metodologii Agile/Scrum
- Wykształcenie wyższe techniczne (informatyka lub pokrewne)
- Bardzo dobra znajomość języka angielskiego

Mile widziane:
- Doświadczenie z Python i frameworkami (Django, FastAPI)
- Znajomość AWS lub innych platform chmurowych
- Doświadczenie w pracy z mikroserwisami
- Certyfikaty techniczne (AWS, MongoDB, itp.)
- Znajomość GraphQL
- Doświadczenie w prowadzeniu zespołu

Oferujemy:
- Atrakcyjne wynagrodzenie adekwatne do umiejętności i doświadczenia
- Elastyczne godziny pracy i możliwość pracy zdalnej
- Prywatną opiekę medyczną i kartę sportową
- Budżet szkoleniowy i możliwość rozwoju zawodowego
- Pracę przy ciekawych i ambitnych projektach
- Przyjazną atmosferę pracy w dynamicznym zespole
- Nowoczesny sprzęt komputerowy

Umiejętności techniczne:
- JavaScript
- TypeScript
- React
- Node.js
- Python
- SQL
- NoSQL
- Docker
- Kubernetes
- CI/CD
- Git
- REST API
- Agile/Scrum
"""

# Zapisywanie przykładowych plików
def create_sample_files():
    """
    Tworzy przykładowe pliki CV i ogłoszeń o pracę.
    """
    # Zapisywanie przykładowego CV
    cv_path = os.path.join(SAMPLE_DIR, "przyklad_cv.txt")
    with open(cv_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_CV)
    
    # Zapisywanie przykładowego ogłoszenia
    job_path = os.path.join(SAMPLE_DIR, "przyklad_ogloszenie.txt")
    with open(job_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_JOB)
    
    print(f"Przykładowe pliki zostały utworzone w katalogu: {SAMPLE_DIR}")
    print(f"CV: {cv_path}")
    print(f"Ogłoszenie: {job_path}")

if __name__ == "__main__":
    create_sample_files()
