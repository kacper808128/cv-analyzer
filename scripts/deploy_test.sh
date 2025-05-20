#!/bin/bash

# Skrypt do testowego wdrożenia aplikacji CV Analyzer
# Skrypt sprawdza poprawność konfiguracji Docker i przeprowadza testowe wdrożenie

echo "=== CV Analyzer - Testowe wdrożenie ==="
echo "Sprawdzanie konfiguracji Docker..."

# Sprawdzenie czy Docker jest zainstalowany
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker nie jest zainstalowany. Zainstaluj Docker i spróbuj ponownie."
    exit 1
fi

# Sprawdzenie czy Docker Compose jest zainstalowany
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose nie jest zainstalowany. Zainstaluj Docker Compose i spróbuj ponownie."
    exit 1
fi

echo "Docker i Docker Compose są zainstalowane."

# Zatrzymanie istniejących kontenerów (jeśli istnieją)
echo "Zatrzymywanie istniejących kontenerów..."
docker-compose down

# Budowanie obrazów
echo "Budowanie obrazów Docker..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "ERROR: Błąd podczas budowania obrazów Docker."
    exit 1
fi

# Uruchamianie kontenerów
echo "Uruchamianie kontenerów..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "ERROR: Błąd podczas uruchamiania kontenerów."
    exit 1
fi

# Czekanie na uruchomienie usług
echo "Czekanie na uruchomienie usług..."
sleep 10

# Sprawdzanie statusu kontenerów
echo "Sprawdzanie statusu kontenerów..."
docker-compose ps

# Sprawdzanie dostępności API
echo "Sprawdzanie dostępności API..."
curl -s http://localhost:8000/health

if [ $? -ne 0 ]; then
    echo "ERROR: API nie jest dostępne."
    exit 1
fi

echo ""
echo "=== Testowe wdrożenie zakończone pomyślnie ==="
echo "Backend API dostępne pod adresem: http://localhost:8000"
echo "Frontend dostępny pod adresem: http://localhost"
echo ""
echo "Aby zatrzymać aplikację, użyj polecenia: docker-compose down"
