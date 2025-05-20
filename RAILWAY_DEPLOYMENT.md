# Instrukcja wdrożenia CV Analyzer na Railway

Ta instrukcja zawiera szczegółowe kroki do wdrożenia aplikacji CV Analyzer na platformie Railway jako dwie osobne usługi (backend i frontend), co jest zalecanym podejściem ze względu na ograniczenia Railway dotyczące użycia `docker-compose` i instrukcji `VOLUME`.

## Przygotowanie

1. Utwórz konto na [Railway.app](https://railway.app/) (możesz zalogować się przez GitHub)
2. Upewnij się, że masz kod aplikacji w repozytorium GitHub

## Krok 1: Wdrożenie backendu

### 1.1. Utwórz nowy projekt na Railway

1. Po zalogowaniu, kliknij przycisk "New Project" w dashboardzie Railway
2. Wybierz opcję "Deploy from GitHub repo"
3. Wybierz repozytorium z kodem CV Analyzer
4. Kliknij "Configure" zamiast "Deploy Now"

### 1.2. Skonfiguruj wdrożenie backendu

1. W ustawieniach projektu:
   - Ustaw "Root Directory" na `/backend`
   - Ustaw "Service Name" na `cv-analyzer-backend`
   - Wybierz "Start Command": `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Kliknij "Deploy"

### 1.3. Dodaj bazę danych PostgreSQL

1. W dashboardzie projektu, kliknij "New Service"
2. Wybierz "Database" → "PostgreSQL"
3. Poczekaj na utworzenie bazy danych

### 1.4. Skonfiguruj zmienne środowiskowe backendu

1. Przejdź do usługi backendu
2. Kliknij zakładkę "Variables"
3. Dodaj następujące zmienne:
   - `DATABASE_URL`: Skopiuj wartość z sekcji "Connect" bazy danych PostgreSQL
   - `API_HOST`: `0.0.0.0`
   - `API_PORT`: `$PORT` (Railway automatycznie przydziela port)
   - `DEBUG`: `False`

### 1.5. Skonfiguruj Railway Volume dla przesyłanych plików

1. W dashboardzie projektu, kliknij "New"
2. Wybierz "Volume"
3. Ustaw nazwę na `uploads`
4. Ustaw ścieżkę montowania na `/app/uploads`
5. Połącz Volume z usługą backendu

## Krok 2: Wdrożenie frontendu

### 2.1. Utwórz nowy projekt na Railway

1. W dashboardzie Railway, kliknij "New Project"
2. Wybierz opcję "Deploy from GitHub repo"
3. Wybierz to samo repozytorium co dla backendu
4. Kliknij "Configure" zamiast "Deploy Now"

### 2.2. Skonfiguruj wdrożenie frontendu

1. W ustawieniach projektu:
   - Ustaw "Root Directory" na `/frontend`
   - Ustaw "Service Name" na `cv-analyzer-frontend`
   - Wybierz "Builder" jako "Nixpacks"
   - Kliknij "Deploy"

### 2.3. Skonfiguruj zmienne środowiskowe frontendu

1. Przejdź do usługi frontendu
2. Kliknij zakładkę "Variables"
3. Dodaj zmienną:
   - `REACT_APP_API_URL`: URL backendu (znajdziesz go w zakładce "Settings" usługi backendu, sekcja "Domains")

## Krok 3: Połączenie usług

### 3.1. Skonfiguruj CORS w backendzie

1. Przejdź do usługi backendu
2. Kliknij zakładkę "Variables"
3. Dodaj zmienną:
   - `CORS_ORIGINS`: URL frontendu (znajdziesz go w zakładce "Settings" usługi frontendu, sekcja "Domains")

### 3.2. Skonfiguruj proxy w frontendzie (opcjonalnie)

Jeśli frontend ma przekierowywać żądania API do backendu, możesz dodać plik `_redirects` w katalogu `public` frontendu:

```
/api/*  https://twoj-backend-url.railway.app/:splat  200
```

## Krok 4: Testowanie wdrożenia

1. Otwórz URL frontendu w przeglądarce (znajdziesz go w zakładce "Settings" usługi frontendu, sekcja "Domains")
2. Przetestuj funkcjonalność aplikacji:
   - Prześlij przykładowe CV i ogłoszenie o pracę
   - Sprawdź, czy analiza działa poprawnie
   - Sprawdź, czy dane są zapisywane w bazie danych

## Rozwiązywanie problemów

### Problem: Backend nie może połączyć się z bazą danych

1. Sprawdź zmienną `DATABASE_URL` w ustawieniach backendu
2. Upewnij się, że baza danych PostgreSQL jest uruchomiona
3. Sprawdź logi backendu, aby zobaczyć szczegóły błędu

### Problem: Frontend nie może połączyć się z backendem

1. Sprawdź zmienną `REACT_APP_API_URL` w ustawieniach frontendu
2. Upewnij się, że backend jest uruchomiony
3. Sprawdź ustawienia CORS w backendzie

### Problem: Pliki przesłane przez użytkowników nie są zachowywane

1. Upewnij się, że Volume jest poprawnie skonfigurowany i podłączony do usługi backendu
2. Sprawdź logi backendu, aby zobaczyć szczegóły błędu

## Uwagi

- Railway oferuje darmowy kredyt $5 miesięcznie, co powinno wystarczyć na testy
- Aplikacje na darmowym planie są usypiane po okresie nieaktywności
- Aby uniknąć uśpienia, możesz skonfigurować "Health Check" dla usług
