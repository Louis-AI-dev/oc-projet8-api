import streamlit as st
import requests
from PIL import Image
import io
import numpy as np
import pickle

# Charger la liste des couleurs
with open("colors_list.pkl", "rb") as f:
    colors = pickle.load(f)

def apply_colormap(mask, colors):
    h, w = mask.shape
    color_mask = np.zeros((h, w, 3), dtype=np.float32)
    for class_index, color in enumerate(colors):
        color_mask[mask == class_index] = color
    return (color_mask * 255).astype(np.uint8)

# Titre principal
st.title("Segmentation d’image")

# Chargement de l’image
uploaded_file = st.file_uploader("Choisissez une image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Image originale", use_column_width=True)

    # Convertir l’image en bytes
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    files = {"image": ("image.png", buffered.getvalue(), "image/png")}
    
    response = requests.post("https://oc-projet8-5ca0c95.onrender.com/predict", files=files)


    if response.status_code == 200:
        try:
            json_response = response.json()
            mask_list = json_response["mask"]
            mask_array = np.array(mask_list, dtype=np.uint8)

            colored_mask = apply_colormap(mask_array, colors)

            # Affichage
            st.image(colored_mask, caption="Masque coloré", use_column_width=256)
        except Exception as e:
            st.error(f"Erreur de décodage du masque : {e}")
    else:
        st.error(f"Erreur lors de l'appel à l'API : {response.status_code} - {response.text}")

