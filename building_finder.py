import cv2
import numpy as np
import matplotlib.pyplot as plt
from util import show_image
from enum import Enum

class ColorRange(Enum):
    GRAY = ((0, 0, 40), (180, 100, 240))
    BLACK = ((0, 0, 0), (180, 255, 30))

def get_color_mask(img, low, high):
    blur = cv2.blur(img, (5,5))
    blur0 = cv2.medianBlur(blur,5)
    blur1 = cv2.GaussianBlur(blur0,(5,5),0)
    blur2 = cv2.bilateralFilter(blur1,9,75,75)
    hsv = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low, high)
    return mask

def remove_color(img, color):
    low, high = map(np.array, color.value)
    color_mask = get_color_mask(img, low, high)
    inverted_color_mask = cv2.bitwise_not(color_mask)
    removed_color = cv2.bitwise_and(img, img, mask=inverted_color_mask)
    return removed_color

def find_contours(img):
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    buildings = {}
    for contour in contours:
        area = cv2.contourArea(contour)
        _,_,w,h = cv2.boundingRect(contour)
        bounding_area = w * h
        max_ratio = 4
        if 1000 <= area <= 12000 and bounding_area < max_ratio * area:
            M = cv2.moments(contour) 
            if M['m00'] != 0.0: 
                x = int(M['m10']/M['m00']) 
                y = int(M['m01']/M['m00']) 
            coordinates = (x, y)
            cv2.putText(img_copy, str(coordinates), coordinates, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1) 
            cv2.drawContours(img_copy, [contour], 0, (0, 0, 255), 2)
            buildings[coordinates] = crop_contour(img, contour)
    show_image(img_copy)
    return buildings

def crop_contour(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = img[y:y+h, x:x+w]
    return cropped_image

def find_buildings(img):
    img_copy = img.copy()
    no_gray = remove_color(img_copy, ColorRange.GRAY)
    no_black = remove_color(no_gray, ColorRange.BLACK)
    buildings = find_contours(no_black)
    return buildings

