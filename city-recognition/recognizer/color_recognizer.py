import cv2
import numpy as np
from sklearn.cluster import KMeans
from .util import Color

def closest_color_name(color):
    closest_name = None
    min_dist = float('inf')
    
    for rgb in Color:
        dist = np.sqrt(np.sum((np.array(color) - np.array(rgb.value))**2))
        if dist < min_dist:
            min_dist = dist
            closest_name = rgb.name
            
    return closest_name

def get_dominant_color(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)
    non_black_pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]

    kmeans = KMeans(n_clusters=1)
    kmeans.fit(non_black_pixels)
    colors = kmeans.cluster_centers_
    
    return colors.astype(int)[0]

def get_color(img):
    color = get_dominant_color(img)
    color_name = closest_color_name(color)
    return color_name