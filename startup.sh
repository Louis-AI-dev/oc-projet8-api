#!/bin/bash

echo "------ Startup script is running ------"

# Optionnel : affiche le contenu du répertoire courant pour vérifier que tout est là
echo "Current directory contents:"
ls -la

# Lancement de Gunicorn avec FastAPI
gunicorn --bind=0.0.0.0:8000 --timeout 600 api:app

echo "------ Gunicorn has been launched ------"