# Dockerfile dla frontendu aplikacji CV Analyzer
FROM node:20-alpine as build

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików zależności
COPY frontend/package.json frontend/package-lock.json ./

# Instalacja zależności
RUN npm ci

# Kopiowanie kodu aplikacji
COPY frontend/ ./

# Budowanie aplikacji
RUN npm run build

# Etap produkcyjny
FROM nginx:alpine

# Kopiowanie zbudowanych plików do katalogu serwera nginx
COPY --from=build /app/build /usr/share/nginx/html

# Kopiowanie konfiguracji nginx
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Ekspozycja portu
EXPOSE 80

# Uruchomienie serwera nginx
CMD ["nginx", "-g", "daemon off;"]
