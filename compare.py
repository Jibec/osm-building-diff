#!/usr/bin/env python3

from skimage.io import imread, imsave
import numpy as np

# Charger les images
osm = imread('osm-buildings.png')
cadastre = imread('cadastre-buildings.png')

# Vérification des dimensions
if osm.shape != cadastre.shape:
    raise ValueError("Les deux images doivent avoir les mêmes dimensions.")

# Masques des pixels strictement noirs (R=G=B=0 et A=255)
osm_black = np.all(osm == [0, 0, 0, 255], axis=-1)
cad_black = np.all(cadastre == [0, 0, 0, 255], axis=-1)

# Pixels noirs dans osm mais pas dans cadastre
osm_only_mask = osm_black & ~cad_black

# Pixels noirs dans cadastre mais pas dans osm
cad_only_mask = cad_black & ~osm_black

# Créer des images blanches opaques (RGBA)
height, width = osm.shape[:2]
white = np.ones((height, width, 4), dtype=np.uint8) * 255  # Blanc opaque

# Appliquer les masques (mettre du noir opaque là où c'est "only")
osm_only_img = white.copy()
osm_only_img[osm_only_mask] = [0, 0, 0, 255]  # noir opaque

cad_only_img = white.copy()
cad_only_img[cad_only_mask] = [0, 0, 0, 255]  # noir opaque

# Sauvegarder les résultats
imsave('osm-only.png', osm_only_img)
imsave('cadastre-only.png', cad_only_img)

print("Images générées : osm-only.png et cadastre-only.png")
