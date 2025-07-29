import tensorflow as tf
import numpy as np

def prepare_image(image, target_size=(256, 256)):
    """
    image : objet PIL.Image
    """
    # Convertir l'image PIL en tableau numpy
    image = np.array(image)

    # Convertir en tenseur
    image = tf.convert_to_tensor(image)

    # Redimensionner
    image = tf.image.resize(image, target_size)

    # Normaliser
    image = tf.cast(image, tf.float32) / 255.0

    # Ajouter la dimension batch
    image = tf.expand_dims(image, axis=0)

    return image
