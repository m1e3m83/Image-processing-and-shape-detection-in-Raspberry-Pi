import cv2 as cv
path = "image/images.png"

image = cv.imread(path)
cv.imshow("image", image)
