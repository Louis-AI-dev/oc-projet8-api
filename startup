#!/bin/bash

echo "------ Startup script is running ------"

echo "Date : $(date)"
echo "Running in: $(pwd)"
echo "Contents:"
ls -la

echo "Launching Gunicorn..."
exec gunicorn --bind=0.0.0.0:8000 --timeout 600 api:app