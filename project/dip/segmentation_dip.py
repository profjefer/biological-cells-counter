import cv2
import numpy as np


def segmentation(image):
    kernel_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(image, -1, kernel_1)
    gauss_image = cv2.GaussianBlur(sharpened_image, (5, 5), 0)
    threshold, otsu_image = cv2.threshold(gauss_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu_image
