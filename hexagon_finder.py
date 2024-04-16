import cv2 
import numpy as np 
from matplotlib import pyplot as plt 

def read_image(img_path):
    img = cv2.imread(img_path) 
    return img

def show_image(img):
    img_copy = img.copy()
    resized = resize_img(img_copy)
    cv2.imshow('shapes', resized) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resize_img(raw_img, target_size = 800):
   h, w = raw_img.shape[:2]
   ratio = min(target_size / w, target_size / h)
   resized = cv2.resize(raw_img, (int(w * ratio), int(h * ratio)))
   return resized

def show_hexagons(hexagons):
    for hexagon in hexagons.values():
        cv2.imshow('masked image', hexagon)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

def remove_background(img):
    img_copy = img.copy()
    hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

    # Thresholds for the greenscreen color
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])

    # Create a mask that distinguishes background and the city
    mask = cv2.inRange(hsv, lower_green, upper_green)
    inverted_mask = cv2.bitwise_not(mask)   

    # Remove noise
    contours, _ = cv2.findContours(inverted_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    largest_contour_mask = np.zeros(inverted_mask.shape, dtype=np.uint8)
    cv2.drawContours(largest_contour_mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

    # Apply the mask to the original image
    result = cv2.bitwise_and(img_copy, img_copy, mask=largest_contour_mask)
    return result

def find_contours(img):
    blurred = cv2.GaussianBlur(img, (13,13), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,5,30)
    kernel = np.ones((13,13), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    return contours

def extract_hexagon_image(contour, img):
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
    masked_image = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = masked_image[y:y+h, x:x+w]
    return cropped_image

def identify_hexagons(img):
    img_copy = img.copy()
    no_background = remove_background(img)
    contours = find_contours(no_background)

    hexagons = {}
    for contour in contours:
        if cv2.contourArea(contour) >= 50:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True) 
            if len(approx) == 6: 
                M = cv2.moments(contour) 
                if M['m00'] != 0.0: 
                    x = int(M['m10']/M['m00']) 
                    y = int(M['m01']/M['m00']) 
                coordinates = str(x) + "," + str(y)
                cv2.putText(img_copy, coordinates, (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1) 
                cv2.drawContours(img_copy, [contour], 0, (0, 0, 255), 2)
                hexagons[coordinates] = extract_hexagon_image(contour, img)

    return hexagons, img_copy

def find_hexagons(img_path, show_results = False):
    img = read_image(img_path)
    hexagons, contour_img = identify_hexagons(img)

    if show_results:
        show_image(contour_img)
        show_hexagons(hexagons)

    return hexagons