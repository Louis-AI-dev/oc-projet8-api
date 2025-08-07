from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
import base64
import os

import sys

import logging

from src.model_loader import model
from src.preprocess import prepare_image

from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger()  # root logger
logger.setLevel(logging.INFO)

# Supprime tous les handlers existants (au cas où)
for h in logger.handlers[:]:
    logger.removeHandler(h)

# Formatter commun
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler console (stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Handler Azure Application Insights (via instrumentation key ou connection string)
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if connection_string:
    azure_handler = AzureLogHandler(connection_string=connection_string)
    azure_handler.setFormatter(formatter)
    logger.addHandler(azure_handler)
    logger.info("Azure Application Insights configuré avec succès.")
else:
    logger.warning("InstrumentationKey manquant : les logs ne seront pas envoyés à Azure Application Insights.")
app = FastAPI()

@app.get("/")
def hello():
    return 'Hello world!'

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    contents = await image.read()
    pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Prétraitement
    input_tensor = prepare_image(pil_image)

    # Prédiction
    prediction = model.predict(input_tensor)[0]  # shape (256, 256, 8)

    # Masque brut (catégorie la plus probable)
    mask = np.argmax(prediction, axis=-1).astype(np.uint8)  # shape (256, 256)

    # On convertit le masque en une liste pour l'envoyer dans la réponse JSON
    return JSONResponse(content={"mask": mask.tolist()})


