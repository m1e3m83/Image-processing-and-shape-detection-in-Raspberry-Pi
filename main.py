import cv2 as cv
#opencv

cap = cv.VideoCapture(0)
path = "image/image.png"
scale = 1
i = 0
read_from_cam = True

while True:
    if read_from_cam:
        _, image = cap.read()
    else:
        image = cv.imread(path)
    img = cv.bitwise_not(image)
    imgBlur = cv.GaussianBlur(img, (7, 7), 1)
    imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgGray, 127, 255, 0)
    #thresh = cv.adaptiveThreshold(imgGray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        continue
    i %= len(contours)

    drawing = image.copy()
    try:
        cv.drawContours(image, contours, i, (0, 255, 0), 5)
    except:
        pass

    cv.imshow("shape", image)
    print(cv.contourArea(contours[i]) / scale * scale)

    key = cv.waitKeyEx(1)
    if key == ord('q'):
        break
    elif key == ord('i'):
        i += 1
    elif key == ord('r'):
        i = 0


cv.destroyAllWindows()


def next_element():
    if hierarchy[i][2] and hierarchy[hierarchy[i][2]][0] != -1:
        return hierarchy[i][2]
    elif hierarchy[i][0] != -1:
        return hierarchy[i][0]
    else:
        return hierarchy[i][3]
