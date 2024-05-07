import cv2
import numpy as np
from digital_grid_builder import build_hexagon_grid
import matplotlib.pyplot as plt

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

# def extract_color(img, low, high):
#     blur = cv2.blur(img, (5,5))
#     blur0 = cv2.medianBlur(blur,5)
#     blur1 = cv2.GaussianBlur(blur0,(5,5),0)
#     blur2 = cv2.bilateralFilter(blur1,9,75,75)
#     hsv = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
#     mask = cv2.inRange(hsv, low, high)
#     result = cv2.bitwise_and(img, img, mask=mask)
#     return result

def get_color_mask(img, low, high):
    blur = cv2.blur(img, (5,5))
    blur0 = cv2.medianBlur(blur,5)
    blur1 = cv2.GaussianBlur(blur0,(5,5),0)
    blur2 = cv2.bilateralFilter(blur1,9,75,75)
    hsv = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, low, high)
    return mask

def extract_color(img, low, high):
    color_mask = get_color_mask(img, low, high)
    color_only = cv2.bitwise_and(img, img, mask=color_mask)

    inverted_color_mask = cv2.bitwise_not(color_mask)
    removed_color = cv2.bitwise_and(img, img, mask=inverted_color_mask)

    # show_image(color_only)
    return color_only, removed_color

def find_contours(img):
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    shapes = {}
    for contour in contours:
        area = cv2.contourArea(contour)
        _,_,w,h = cv2.boundingRect(contour)
        bounding_area = w * h
        max_ratio = 2
        if 1000 <= area <= 5000 and bounding_area < 3 * area:
            M = cv2.moments(contour) 
            if M['m00'] != 0.0: 
                x = int(M['m10']/M['m00']) 
                y = int(M['m01']/M['m00']) 
            coordinates = (x, y)
            cv2.putText(img_copy, str(coordinates), coordinates, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 0, 0), 1) 
            cv2.drawContours(img_copy, [contour], 0, (0, 0, 255), 2)
            shapes[coordinates] = []
    # show_image(img_copy)
    return shapes, img_copy


def plot_coords(coords):
    x_values = [coord[0] for coord in coords]
    y_values = [coord[1] for coord in coords]

    plt.scatter(x_values, y_values, color='blue', label='coords')

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot of Coordinates')

    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    # plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()

img = cv2.imread('resources/stad1.png')
img_copy = img.copy()

green_only, img_copy = extract_color(img_copy, np.array([35, 50, 50]), np.array([75, 255, 255]))
blue_only, img_copy = extract_color(img_copy, np.array([90, 80, 80]), np.array([130, 255, 255])) 
yellow_only, img_copy = extract_color(img_copy, np.array([22, 100, 100]), np.array([45, 255, 255]))
orange_only, img_copy = extract_color(img_copy, np.array([10, 100, 100]), np.array([22, 255, 255]))
white_only, img_copy = extract_color(img_copy, np.array([0,0,215]), np.array([180,120,255]))
brown_only, img_copy = extract_color(img_copy, np.array([3, 100, 50]), np.array([20, 220, 255]))
red_only, img_copy = extract_color(img_copy, np.array([0, 100, 100]), np.array([255, 255, 255]))

green_shapes, green_contour_image = find_contours(green_only)
blue_shapes, blue_contour_image = find_contours(blue_only)
yellow_shapes, yellow_contour_image = find_contours(yellow_only)
orange_shapes, orange_contour_image = find_contours(orange_only)
white_shapes, white_contour_image = find_contours(white_only)
brown_shapes, brown_contour_image = find_contours(brown_only)
red_shapes, red_contour_image = find_contours(red_only)


shapes = {**green_shapes, **blue_shapes, **yellow_shapes, **orange_shapes, **white_shapes, **brown_shapes, **red_shapes}
hexagon_grid = build_hexagon_grid(shapes.keys(), img)
