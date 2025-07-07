#!/usr/bin/env python3

import numpy as np
from skimage import io, img_as_ubyte

def extraire_et_noircir_couleur(image_path, building_color, tolérance=0):
    """
    Remplace une couleur par du noir et rend le reste de l'image transparent.

    Args:
        image_path (str): Chemin de l'image PNG.
        building_color (tuple): Couleur cible à remplacer (R, G, B) [0-255].
        tolérance (int): Tolérance pour la détection de la couleur.

    Returns:
        ndarray: Image avec pixels noirs à la place de la couleur cible, le reste transparent.
    """
    # Charger l'image
    image = io.imread(image_path)

    if image.shape[2] == 3:
        # Ajouter canal alpha si absent
        alpha = np.ones((image.shape[0], image.shape[1], 1), dtype=np.uint8) * 255
        image = np.concatenate((image, alpha), axis=2)

    image = image.astype(np.uint8)
    building_color = np.array(building_color)

    # Création du masque
    masque = np.all(np.abs(image[..., :3] - building_color) <= tolérance, axis=-1)

    # Créer une image de sortie entièrement transparente
    resultat = np.zeros_like(image)
    resultat[..., 3] = 0  # Alpha transparent partout

    # Mettre les pixels correspondants en noir opaque
    resultat[masque] = [0, 0, 0, 255]

    return resultat

# Exemple d'utilisation :
image_resultat = extraire_et_noircir_couleur("osm.png", building_color=(212, 203, 203), tolérance=0)

# Sauvegarder le résultat
io.imsave("osm-buildings.png", img_as_ubyte(image_resultat))

image_resultat = extraire_et_noircir_couleur("cadastre.png", building_color=(255, 204, 51), tolérance=0)
io.imsave("cadastre-buildings.png", img_as_ubyte(image_resultat))