#!/usr/bin/env python3
from skimage import io, measure
import numpy as np


def filter_small_shapes(input_path, output_path, min_size=10):
    # Charger l'image en niveaux de gris
    img = io.imread(input_path, as_gray=True)

    # Binariser l'image (seuil à 0.5 par défaut)
    binary = img < 0.5  # formes noires = True, fond blanc = False

    # Étiqueter les objets connexes
    labeled_img = measure.label(binary)

    # Calculer les régions
    regions = measure.regionprops(labeled_img)

    # Créer une nouvelle image binaire vide
    filtered = np.zeros_like(binary, dtype=bool)

    # Conserver uniquement les régions plus grandes que min_size
    for region in regions:
        if region.area_filled >= min_size:
            filtered[labeled_img == region.label] = True

    # Sauvegarder l'image filtrée (noir/blanc)
    # Ici on inverse car True = noir, False = blanc
    io.imsave(output_path, (~filtered).astype(np.uint8) * 255)


if __name__ == "__main__":
    min_size = 200
    print(f"Filtrage des formes de taille minimale {min_size} pixels...")
    filter_small_shapes("osm-only.png", f"osm-only-filtered-{min_size}.png", min_size=min_size)
    filter_small_shapes("cadastre-only.png", f"cadastre-only-filtered-{min_size}.png", min_size=min_size)
    print(f"Images filtrées sauvegardées : osm-only-filtered-{min_size}.png et cadastre-only-filtered-{min_size}.png")