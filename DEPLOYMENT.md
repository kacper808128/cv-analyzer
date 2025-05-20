# CV Analyzer - Dokumentacja wdrożeniowa

## Wprowadzenie

Ten dokument zawiera instrukcje dotyczące wdrażania aplikacji CV Analyzer w środowisku produkcyjnym przy użyciu Docker i Docker Compose. Aplikacja składa się z trzech głównych komponentów:

1. Backend API (FastAPI)
2. Frontend (React)
3. Baza danych (PostgreSQL)

## Wymagania systemowe

- Docker Engine (wersja 20.10.0 lub nowsza)
- Docker Compose (wersja 2.0.0 lub nowsza)
- Minimum 2GB RAM
- Minimum 10GB wolnego miejsca na dysku

## Struktura plików wdrożeniowych

```
my-cv-analyzer/
├── backend/
│   ├── Dockerfile        # Plik Dockerfile dla backendu
│   └── ...
├── frontend/
│   ├── Dockerfile        # Plik Dockerfile dla frontendu
│   ├── nginx.conf        # Konfiguracja serwera Nginx
│   └── ...
├── .github/
│   └── workflows/
│       └── ci.yml        # Konfiguracja CI/CD dla GitHub Actions
├── docker-compose.yml    # Konfiguracja Docker Compose
├── scripts/
│   └── deploy_test.sh    # Skrypt do testowego wdrożenia
└── ...
```

## Konfiguracja środowiska

Przed wdrożeniem aplikacji należy skonfigurować odpowiednie zmienne środowiskowe. W środowisku produkcyjnym zaleca się utworzenie pliku `.env` w katalogu głównym projektu z następującymi zmiennymi:

```
# Baza danych
POSTGRES_USER=postgres
POSTGRES_PASSWORD=silne_haslo
POSTGRES_DB=cv_analyzer

# Backend API
DATABASE_URL=postgresql://postgres:silne_haslo@db/cv_analyzer
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Frontend
REACT_APP_API_URL=http://api.twoja-domena.pl
```

## Instrukcje wdrożenia

### Wdrożenie lokalne (testowe)

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/twoj-uzytkownik/my-cv-analyzer.git
   cd my-cv-analyzer
   ```

2. Uruchom skrypt testowego wdrożenia:
   ```bash
   ./scripts/deploy_test.sh
   ```

3. Aplikacja będzie dostępna pod adresami:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost

### Wdrożenie produkcyjne

1. Sklonuj repozytorium na serwerze produkcyjnym:
   ```bash
   git clone https://github.com/twoj-uzytkownik/my-cv-analyzer.git
   cd my-cv-analyzer
   ```

2. Utwórz plik `.env` z konfiguracją produkcyjną (patrz sekcja "Konfiguracja środowiska").

3. Zbuduj i uruchom kontenery:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

4. Skonfiguruj serwer proxy (np. Nginx) do przekierowywania ruchu do odpowiednich kontenerów.

## Aktualizacja aplikacji

Aby zaktualizować aplikację do najnowszej wersji:

1. Pobierz najnowsze zmiany z repozytorium:
   ```bash
   git pull origin main
   ```

2. Przebuduj i uruchom kontenery:
   ```bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   ```

## Monitorowanie i logi

Aby sprawdzić logi aplikacji:

```bash
# Logi wszystkich kontenerów
docker-compose logs

# Logi konkretnego kontenera
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

## Rozwiązywanie problemów

### Problem: Kontenery nie uruchamiają się

1. Sprawdź logi kontenerów:
   ```bash
   docker-compose logs
   ```

2. Upewnij się, że porty nie są zajęte przez inne aplikacje:
   ```bash
   netstat -tuln | grep '8000\|80\|5432'
   ```

### Problem: Backend nie może połączyć się z bazą danych

1. Sprawdź zmienne środowiskowe w pliku `.env`.
2. Upewnij się, że kontener bazy danych jest uruchomiony:
   ```bash
   docker-compose ps db
   ```

## Kopie zapasowe

Aby utworzyć kopię zapasową bazy danych:

```bash
docker-compose exec db pg_dump -U postgres cv_analyzer > backup.sql
```

Aby przywrócić bazę danych z kopii zapasowej:

```bash
cat backup.sql | docker-compose exec -T db psql -U postgres cv_analyzer
```

## Bezpieczeństwo

W środowisku produkcyjnym należy:

1. Zmienić domyślne hasła bazy danych.
2. Skonfigurować HTTPS dla frontendu i backendu.
3. Ograniczyć dostęp do API tylko do zaufanych źródeł.
4. Regularnie aktualizować obrazy Docker, aby zawierały najnowsze poprawki bezpieczeństwa.
