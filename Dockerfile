# Image Python officielle légère
FROM python:3.12

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source et le modèle (fichier .h5)
COPY api.py .
COPY src/ ./src/
COPY 1_best_unet_baseline.h5 .

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Lancer l'application FastAPI (api.py doit contenir "app = FastAPI()")
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
