import cv2
import numpy as np
from .util import Color

# A very naive way of finding the color of the building. 
# It computes the vector distance to the each of the RGB values of all the used colors 
# (Colors are defined in util.py)
def closest_color_name(color):
    closest_name = None
    min_dist = float('inf')
    
    for rgb in Color:
        dist = np.sqrt(np.sum((np.array(color) - np.array(rgb.value))**2))
        if dist < min_dist:
            min_dist = dist
            closest_name = rgb.name
            
    return closest_name

# KNN: (k=1)
def initialize_centroids(pixels, k):
    return pixels[np.random.choice(pixels.shape[0], k, replace=False)]

def assign_clusters(pixels, centroids):
    distances = np.linalg.norm(pixels - centroids[:, np.newaxis], axis=2)
    return np.argmin(distances, axis=0)

def update_centroids(pixels, clusters, k):
    new_centroids = np.array([pixels[clusters == i].mean(axis=0) for i in range(k)])
    return new_centroids

def kmeans(pixels, k, max_iters=100, tol=1e-4):
    centroids = initialize_centroids(pixels, k)
    for _ in range(max_iters):
        clusters = assign_clusters(pixels, centroids)
        new_centroids = update_centroids(pixels, clusters, k)
        if np.all(np.abs(new_centroids - centroids) < tol):
            break
        centroids = new_centroids
    return centroids

def get_dominant_color(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3)
    non_black_pixels = pixels[np.any(pixels != [0, 0, 0], axis=1)]
    dominant_color = kmeans(non_black_pixels, k=1)[0]
    return dominant_color.astype(int)


def get_color(img):
    color = get_dominant_color(img)
    color_name = closest_color_name(color)
    return color_name