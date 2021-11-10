import cv2
import numpy as np


def otsu_thresh(img):
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def niblack_thresh(img):
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    res = img.copy()
    thresh_niblack = cv2.ximgproc.niBlackThreshold(img, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=2 * 11 + 1,
                                                   k=-0.2, binarizationMethod=cv2.ximgproc.BINARIZATION_NICK)

    binary_niblack = img > thresh_niblack

    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            if binary_niblack[i][j] == True:
                res[i][j] = 255
            else:
                res[i][j] = 0
    return res


def sauvola_thresh(img):
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    res = img.copy()
    thresh_sauvola = cv2.ximgproc.niBlackThreshold(img, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=2 * 11 + 1,
                                                   k=-0.2, binarizationMethod=cv2.ximgproc.BINARIZATION_SAUVOLA)

    binary_sauvola = img > thresh_sauvola

    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            if binary_sauvola[i][j] == True:
                res[i][j] = 255
            else:
                res[i][j] = 0
    return res


def medianBlur15(img):
    image = cv2.imread(img)
    return cv2.medianBlur(image, 15)


def morphology7x7(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    return cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)


def gradientOrientation(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gX = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    gY = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    return np.arctan2(gY, gX) * (180 / np.pi) % 180


def cannyWide(img):
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.Canny(blurred, 10, 200)
