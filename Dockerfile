# Image Python officielle légère
FROM python:3.12-slim

# Empêcher Python de générer des fichiers .pyc et activer un stdout non bufferisé
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source et le modèle (fichier .h5)
COPY api.py .
COPY src/ ./src/
COPY 1_best_unet_baseline.h5 .

# Exposer le port (optionnel, surtout utile en local)
EXPOSE 8000

# Lancer l'application FastAPI avec le port fourni par Render
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]

