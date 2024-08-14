import cv2
from enum import Enum

class Color(Enum):
    RED = (255, 0, 0)
    GREEN = (20, 60, 20)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 125, 0)
    BROWN = (80, 40, 30)
    WHITE = (255, 255, 255)

def show_image(img, target_size = 800):
    img_copy = img.copy()
    resized = resize_img(img_copy, target_size)
    cv2.imshow('shapes', resized) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_img(raw_img, target_size):
   h, w = raw_img.shape[:2]
   ratio = min(target_size / w, target_size / h)
   resized = cv2.resize(raw_img, (int(w * ratio), int(h * ratio)))
   return resized
