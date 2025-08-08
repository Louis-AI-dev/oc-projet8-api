from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io

from src.model_loader import model
from src.preprocess import prepare_image

import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

logger.info("✅ Application démarrée")

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello world!"}

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


