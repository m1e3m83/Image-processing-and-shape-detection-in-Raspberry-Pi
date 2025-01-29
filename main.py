import cv2 as cv
import numpy as np

scale_num = 0


def find_scale(img):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    #cv.imshow("Unprocessed Image", img)

    # Define HSV range for red
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])

    # Create masks for both red ranges
    mask1 = cv.inRange(hsv, lower1, upper1)
    mask2 = cv.inRange(hsv, lower2, upper2)
    mask = cv.bitwise_or(mask1, mask2)

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    # Apply the mask to the original image
    final = cv.bitwise_and(img, img, mask=mask)
    #cv.imshow("red parts", final)
    #cv.waitKey(0)

    # Convert the filtered image to grayscale

    scale_contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    scale = 1
    if len(scale_contours) > 0:
        scale = cv.arcLength(scale_contours[scale_num % len(scale_contours)], True) / 2
    cv.drawContours(image, scale_contours, 0, (0, 0, 255), -1)
    return scale


cap = cv.VideoCapture(0)
path = "image/image.png"
scale = 1
object_num = 0
read_from_cam = True

font_thicness = 2
org = (50, 50)

while True:
    if read_from_cam:
        _, image = cap.read()
    else:
        image = cv.imread(path)
    #img = image
    img = cv.bitwise_not(image)
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (7, 7), 5)
    ret, thresh = cv.threshold(imgBlur, 0, 255,
                               cv.THRESH_BINARY + cv.THRESH_OTSU)  #cv.threshold(imgGray, 127, 255, 0, )
    #thresh = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    scale = find_scale(image)
    if len(contours) == 0:
        continue
    object_num %= len(contours)

    area = cv.contourArea(contours[object_num]) / scale / scale

    try:
        cv.drawContours(image, contours, object_num, (0, 255, 0), 5)
        cv.putText(image, "Area = " + str(area), org, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), font_thicness,
                   cv.LINE_AA)
    except:
        pass

    cv.imshow("shape", image)
    #print("area: " + str(area) + "| scale: " + str(scale))

    key = cv.waitKeyEx(1)
    if key == ord('q'):
        break
    elif key == ord('i'):
        object_num += 1
    elif key == ord('r'):
        object_num = 0
        scale_num = 0
    elif key == ord('s'):
        scale_num += 1

cv.destroyAllWindows()
