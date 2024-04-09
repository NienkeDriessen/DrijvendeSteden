import cv2 
import numpy as np 
from matplotlib import pyplot as plt 

def read_image(img_path):
    raw_img = cv2.imread(img_path) 
    width = 800
    aspect_ratio = raw_img.shape[1] / raw_img.shape[0]
    height = int(width / aspect_ratio)
    img = cv2.resize(raw_img, (width, height))
    return img

def find_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    return contours

def find_hexagon(contours, img):
    img_copy = img.copy()
    result = {}
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) 
        if len(approx) == 6: 
            M = cv2.moments(contour) 
            if M['m00'] != 0.0: 
                x = int(M['m10']/M['m00']) 
                y = int(M['m01']/M['m00']) 
            coordinates = str(x) + "," + str(y)
            cv2.putText(img_copy, coordinates, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1) 
            cv2.drawContours(img_copy, [contour], 0, (0, 0, 255), 2)
            masked_image = extract_hexagon_image(contour, img)
            result[coordinates] = masked_image
    return result, img_copy
    
def create_mask_from_contour(contour, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
    return mask

def extract_hexagon_image(contour, img):
    mask = create_mask_from_contour(contour, img.shape)
    masked_image = cv2.bitwise_and(img, img, mask=mask)
    cropped_image = crop_to_bounding_box(masked_image, contour)
    return cropped_image

def crop_to_bounding_box(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = img[y:y+h, x:x+w]
    return cropped_image

def find_cells(img):
    img = read_image(img)
    contours = find_contours(img)
    extracted_cells, img_copy = find_hexagon(contours, img)
    return extracted_cells, img_copy

def show_results(img, extracted_cells):
    cv2.imshow('shapes', img) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    for masked_image in extracted_cells.values():
        cv2.imshow('masked image', masked_image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()