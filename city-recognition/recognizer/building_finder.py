import cv2
import numpy as np
from enum import Enum
from .util import debug_show

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

    # Protect bright whites
    v = hsv[:, :, 2]
    bright = v > 200   # may be problematic in different lighting conditions
    mask[bright] = 0

    return mask

def remove_color(img, color, show_debug=False):
    low, high = map(np.array, color.value)
    color_mask = get_color_mask(img, low, high)
    # if show_debug:
    #     debug_show(f"Color Mask for {color.name}", color_mask)
    inverted_color_mask = cv2.bitwise_not(color_mask)
    removed_color = cv2.bitwise_and(img, img, mask=inverted_color_mask)

    
    return removed_color


def find_contours(img, show_debug=False):
    img_copy = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    if show_debug:
        debug_show("Binary Image", binary_image)

    contours, _ = cv2.findContours(
        binary_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    img_area = img.shape[0] * img.shape[1]
    min_area_ratio_basic = 0.0005
    # --- First, collect all areas for median calculation ---
    all_contour_data = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h if h > 0 else 0

        if area / img_area < min_area_ratio_basic:
            continue
        all_contour_data.append({
            "contour": contour,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "bbox": (x, y, w, h),
        })

    if not all_contour_data:
        return {}

    # --- Compute median area ---
    areas = np.array([c["area"] for c in all_contour_data])
    median_area_ratio =  np.median(areas) / img_area
    print("Median area ratio:", median_area_ratio)

    min_area_ratio = 0.5 * median_area_ratio
    max_area_ratio = 3.0 * median_area_ratio

    # --- First pass: collect candidates ---
    candidates = []
    rejected = []  

    # to remove the very small ones
    # max_area_ratio = 0.02

    for contour in contours:
        area = cv2.contourArea(contour)
        area_ratio = area / img_area

        if area_ratio < min_area_ratio_basic:
            rejected.append((contour, "area_ratio basic too small"))
            print("Rejected contour due to very small area ratio:", area_ratio)
            continue
        if  area_ratio < min_area_ratio:
            rejected.append((contour, "area_ratio too small"))
            print("Rejected contour due to small area ratio:", area_ratio)
            continue

        if area_ratio > max_area_ratio:
            print("Rejected contour due to large area ratio:", area_ratio)
            rejected.append((contour, "area_ratio too large"))
            continue

        x, y, w, h = cv2.boundingRect(contour)
        bounding_area = w * h

        # Loose sanity check (keeps very broken shapes out)
        if bounding_area > 3.5 * area:
            rejected.append((contour, "bounding_area"))
            continue

        aspect_ratio = w / h if h > 0 else 0

        candidates.append({
            "contour": contour,
            "area": area,
            "aspect_ratio": aspect_ratio,
            "bbox": (x, y, w, h),
        })

    # --- optional: debug show rejected contours ---
    if show_debug and rejected:
        debug_img = img.copy()
        for contour, reason in rejected:
            color = (0, 0, 255)  # red for rejected
            cv2.drawContours(debug_img, [contour], -1, color, 2)
            # label with reason
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(debug_img, reason, (cx, cy),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1)
        debug_show("Rejected Contours", debug_img)
    else: 
        print("No contours were rejected.")

    if not candidates:
        return {}

    areas = np.array([c["area"] for c in candidates])
    median_area = np.median(areas)

    min_area = 0.5 * median_area
    max_area = 2.5 * median_area

    buildings = {}
    rejected_second_pass = []

    for c in candidates:
        area = c["area"]
        ar = c["aspect_ratio"]
        contour = c["contour"]
        

        # Size outlier rejection
        if not (min_area <= area <= max_area):
            rejected_second_pass.append((contour, "size_outlier"))
            print("Rejected contour due to size outlier:", area)
            continue

        # Aspect ratio check (roughly square-ish)
        if not (0.5 <= ar <= 2.0):
            rejected_second_pass.append((contour, "aspect_ratio"))
            print("Rejected contour due to aspect ratio:", ar)
            continue

        M = cv2.moments(contour)
        if M["m00"] == 0:
            rejected_second_pass.append((contour, "zero_area"))
            continue

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        coordinates = (cx, cy)

        cv2.drawContours(img_copy, [contour], -1, (255, 0, 255), 2)

        buildings[coordinates] = crop_contour(img, contour)

    # --- optional debug view for rejected second-pass contours ---
    if show_debug and rejected_second_pass:
        debug_img = img.copy()
        for contour, reason in rejected_second_pass:
            color = (0, 0, 255)  # red for rejected
            cv2.drawContours(debug_img, [contour], -1, color, 2)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(debug_img, reason, (cx, cy),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, color, 1)
        debug_show("Rejected Second-Pass Contours", debug_img)

    if show_debug:
        debug_show("Detected Buildings", img_copy)

    return buildings


def crop_contour(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = img[y:y+h, x:x+w]
    return cropped_image

def find_buildings(img, show_debug=False):
    img_copy = img.copy()

    no_gray = remove_color(img_copy, ColorRange.GRAY, show_debug)
    no_black = remove_color(no_gray, ColorRange.BLACK, show_debug)
    buildings = find_contours(no_black, show_debug)
    
    return buildings

