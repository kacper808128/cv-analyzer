"""
Moduł do tworzenia pliku .env z konfiguracją środowiska.
"""
import os

def create_env_file():
    """
    Tworzy plik .env z konfiguracją środowiska.
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    
    # Domyślna konfiguracja dla lokalnego środowiska deweloperskiego
    env_content = """# Konfiguracja środowiska dla CV Analyzer
# Baza danych
DATABASE_URL=postgresql://postgres:postgres@localhost/cv_analyzer

# Serwer API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Konfiguracja uploadu plików
MAX_UPLOAD_SIZE=10485760  # 10MB w bajtach
"""
    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print(f"Plik .env został utworzony: {env_path}")

if __name__ == "__main__":
    create_env_file()
