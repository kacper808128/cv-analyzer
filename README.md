# CV Analyzer - Analiza CV pod kątem zgodności z ogłoszeniami o pracę

## Opis projektu

CV Analyzer to kompleksowa aplikacja webowa umożliwiająca automatyczną analizę CV pod kątem zgodności z treścią ogłoszenia o pracę. Aplikacja wykorzystuje zaawansowane techniki przetwarzania języka naturalnego (NLP) do oceny relewantności kandydata na podstawie jego CV w odniesieniu do wymagań zawartych w ogłoszeniu.

![CV Analyzer Screenshot](https://via.placeholder.com/800x450.png?text=CV+Analyzer+Screenshot)

## Funkcjonalności

- Upload plików CV i ogłoszeń o pracę (PDF, DOCX, TXT)
- Ekstrakcja kluczowych informacji z dokumentów:
  - Dane kontaktowe
  - Doświadczenie zawodowe
  - Wykształcenie
  - Umiejętności
- Analiza semantycznego podobieństwa między CV a ogłoszeniem
- Ocena relewantności kandydata na podstawie różnych kryteriów:
  - Dopasowanie umiejętności
  - Zgodność doświadczenia
  - Adekwatność wykształcenia
- Wizualizacja wyników analizy
- Podświetlanie słów kluczowych w dokumentach
- Przechowywanie historii analiz

## Architektura projektu

Projekt składa się z trzech głównych części:

1. **Backend** - API REST zbudowane z wykorzystaniem FastAPI (Python)
2. **Frontend** - Interfejs użytkownika zbudowany z wykorzystaniem React (TypeScript)
3. **Baza danych** - PostgreSQL do przechowywania wyników analiz

### Struktura katalogów

```
my-cv-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpointy API
│   │   ├── models/       # Modele ORM
│   │   ├── nlp/          # Moduły NLP i analizy
│   │   ├── services/     # Usługi biznesowe
│   │   ├── main.py       # Główny plik aplikacji
│   ├── scripts/          # Skrypty pomocnicze
│   ├── sample_data/      # Przykładowe dane
│   ├── uploads/          # Katalog na przesłane pliki
│   ├── venv/             # Wirtualne środowisko Python
│   ├── requirements.txt  # Zależności Pythona
│   ├── .env              # Zmienne środowiskowe
│   ├── Dockerfile        # Konfiguracja Docker dla backendu
├── frontend/
│   ├── src/
│   │   ├── components/   # Komponenty React
│   │   ├── pages/        # Strony aplikacji
│   │   ├── services/     # Usługi API
│   │   ├── styles/       # Style CSS
│   ├── public/           # Statyczne zasoby
│   ├── package.json      # Zależności Node.js
│   ├── Dockerfile        # Konfiguracja Docker dla frontendu
│   ├── nginx.conf        # Konfiguracja Nginx
├── .github/
│   └── workflows/
│       └── ci.yml        # Konfiguracja CI/CD
├── docker-compose.yml    # Konfiguracja Docker Compose
├── scripts/              # Skrypty globalne
├── DEPLOYMENT.md         # Dokumentacja wdrożeniowa
├── README.md             # Dokumentacja projektu
```

## Technologie

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- pdfplumber, python-docx (ekstrakcja tekstu)
- spaCy, Transformers (NLP)
- Pytest (testy)

### Frontend
- React
- TypeScript
- CSS (style komponentów)
- Axios (komunikacja z API)

### Deployment
- Docker
- Docker Compose
- GitHub Actions (CI/CD)
- Nginx

## Instalacja i uruchomienie

### Wymagania
- Docker Engine (wersja 20.10.0 lub nowsza)
- Docker Compose (wersja 2.0.0 lub nowsza)

### Uruchomienie z użyciem Docker Compose

1. Sklonuj repozytorium:
```bash
git clone https://github.com/twoj-uzytkownik/my-cv-analyzer.git
cd my-cv-analyzer
```

2. Uruchom aplikację za pomocą Docker Compose:
```bash
docker-compose up -d
```

3. Aplikacja będzie dostępna pod adresami:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost
   - Dokumentacja API (Swagger): http://localhost:8000/docs

### Uruchomienie bez Dockera

#### Backend

1. Przejdź do katalogu backendu:
```bash
cd my-cv-analyzer/backend
```

2. Utwórz i aktywuj wirtualne środowisko Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Utwórz plik .env z konfiguracją:
```bash
python scripts/create_env.py
```

5. Uruchom serwer API:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend

1. Przejdź do katalogu frontendu:
```bash
cd my-cv-analyzer/frontend
```

2. Zainstaluj zależności:
```bash
npm install
```

3. Uruchom serwer deweloperski:
```bash
npm start
```

4. Frontend będzie dostępny pod adresem: http://localhost:3000

## Użytkowanie aplikacji

1. Otwórz aplikację w przeglądarce (http://localhost lub http://localhost:3000 w trybie deweloperskim).

2. Na stronie głównej znajdziesz formularz do przesyłania plików:
   - Wybierz plik CV (PDF, DOCX lub TXT)
   - Wybierz plik ogłoszenia o pracę (PDF, DOCX lub TXT)
   - Kliknij przycisk "Analizuj dopasowanie"

3. Po zakończeniu analizy zobaczysz wyniki:
   - Ogólny wynik dopasowania
   - Wyniki według sekcji (umiejętności, doświadczenie, wykształcenie)
   - Tabelę dopasowania umiejętności
   - Podgląd dokumentów z podświetlonymi słowami kluczowymi

4. Możesz rozpocząć nową analizę, klikając przycisk "Rozpocznij nową analizę".

## Wdrożenie produkcyjne

Szczegółowe instrukcje dotyczące wdrożenia produkcyjnego znajdują się w pliku [DEPLOYMENT.md](DEPLOYMENT.md).

## Rozwój projektu

### Uruchomienie testów

```bash
cd my-cv-analyzer/backend
source venv/bin/activate
pytest app/tests/
```

### Dodawanie nowych funkcjonalności

1. Sklonuj repozytorium i utwórz nową gałąź:
```bash
git clone https://github.com/twoj-uzytkownik/my-cv-analyzer.git
cd my-cv-analyzer
git checkout -b feature/nowa-funkcjonalnosc
```

2. Wprowadź zmiany i przetestuj lokalnie.

3. Wypchnij zmiany i utwórz Pull Request:
```bash
git push origin feature/nowa-funkcjonalnosc
```

## Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdują się w pliku LICENSE.

## Autorzy

Projekt realizowany na zlecenie.
