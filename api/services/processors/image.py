import pytesseract
import cv2
import numpy as np
from PIL import Image


def preprocess_image(image: Image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    adaptive_thresh_img = cv2.adaptiveThreshold(
        gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    blurred_img = cv2.GaussianBlur(adaptive_thresh_img, (5, 5), 0)

    return blurred_img


def extract_text(image: Image):
    processed_image = preprocess_image(image)

    text = pytesseract.image_to_string(processed_image)

    return text
