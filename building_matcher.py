import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def import_building_templates():
   dir = 'resources/buildings/'
   files = os.listdir(dir)
   templates = []
   for file in files:
      path = dir + file
      template = cv2.imread(path, cv2.IMREAD_UNCHANGED)
      templates.append(template)
   return templates


def find_building_contour(img):
   img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
   _, threshold = cv2.threshold(img_gray, 160, 255, cv2.THRESH_BINARY) 
   contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   if len(contours) < 2:
      return []
   return contours[1]

def crop_to_bounding_box(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = img[y:y+h, x:x+w]
    return cropped_image

def create_mask_from_contour(contour, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
    return mask

def preprocess_building(img):
   contour = find_building_contour(img)
   if len(contour) == 0:
      print("could find contour")
      return []
   mask = create_mask_from_contour(contour, img.shape)
   masked_image = cv2.bitwise_and(img, img, mask=mask)
   cropped_image = crop_to_bounding_box(masked_image, contour)
   resized_image = resize_img(cropped_image)
   return resized_image

def preprocess_template(img):
   template_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   _, mask = cv2.threshold(template_gray, 0, 255, cv2.THRESH_BINARY)
   masked_image = cv2.bitwise_and(img, img, mask=mask)
   cropped_image = crop_to_bounding_box(masked_image, template_gray)
   resized_image = resize_img(cropped_image[:,:,:3])
   return resized_image[:,:,:3]

def resize_img(raw_img, target_size = 200):
   h, w = raw_img.shape[:2]
   ratio = min(target_size / w, target_size / h)
   resized = cv2.resize(raw_img, (int(w * ratio), int(h * ratio)))

   canvas = np.ones((target_size, target_size, 3), dtype=np.uint8) * 0
   canvas[0:0+resized.shape[0], 0:0+resized.shape[1]] = resized

   return canvas

def find_closest_match(building_templates, img):
   best_match = None
   best_match_value = -float('inf')
   building_img = preprocess_building(img)
   if len(building_img) == 0:
      best_match = cv2.imread('resources/none.png')
   else:
      for template in building_templates:
         template_img = preprocess_template(template)
         result = cv2.matchTemplate(building_img, template_img, cv2.TM_CCOEFF_NORMED)
         _,max_val,_,_ = cv2.minMaxLoc(result)

         if max_val > best_match_value:
            best_match_value = max_val
            best_match = template

   cv2.imshow('building', img) 
   cv2.imshow('ref', best_match) 
   cv2.waitKey(0)
   cv2.destroyAllWindows()

   return best_match


def match_buildings(img):
   building_templates = import_building_templates()
   find_closest_match(building_templates, img)