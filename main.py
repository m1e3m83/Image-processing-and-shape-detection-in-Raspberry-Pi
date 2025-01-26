import cv2 as cv

path = "image/image.png"
i = 0

img = cv.imread(path)
image = cv.bitwise_not(img)

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv.drawContours(img, contours, 0, (0, 255, 0), 1)

area = []
for contour in contours:
    area.append(cv.contourArea(contour))

print(hierarchy)
print(area)

cv.imshow("image", img)

cv.waitKey(0)
cv.destroyAllWindows()
