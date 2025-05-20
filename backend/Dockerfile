# Dockerfile dla backendu aplikacji CV Analyzer
FROM python:3.11-slim

# Ustawienie zmiennych środowiskowych
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików zależności
COPY backend/requirements.txt .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu aplikacji
COPY backend/app ./app
COPY backend/scripts ./scripts
COPY backend/.env .

# Tworzenie katalogów na przesłane pliki i przykładowe dane
RUN mkdir -p uploads sample_data

# Utworzenie przykładowych plików do testów
RUN python scripts/create_sample_files.py

# Ekspozycja portu
EXPOSE 8000

# Uruchomienie aplikacji
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
