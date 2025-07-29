from tensorflow.keras.models import load_model

# Charge le modèle une seule fois au démarrage
model = load_model("1_best_unet_baseline.h5")