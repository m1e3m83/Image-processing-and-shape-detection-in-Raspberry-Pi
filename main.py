import cv2 as cv

cap = cv.VideoCapture(0)
scale = 1
i = 0


def remove_inner():
    global contours, hierarchy

    filtered_contours = []  # To store only the desired contours
    for i, cnt in enumerate(contours):
        # Check if the contour has a child (hierarchy[i][2] != -1) and that child has no siblings
        if hierarchy[0][i][2] != -1 and hierarchy[0][hierarchy[0][i][2]][0] == -1:
            continue  # Skip adding this contour to filtered_contours
        filtered_contours.append(cnt)

    # Update contours with filtered ones
    contours = filtered_contours

while True:
    _, image = cap.read()

    imgray = cv.cvtColor(cv.bitwise_not(image), cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 63, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = list(contours)
    #remove_inner()

    drawimg = image.copy()
    cv.drawContours(drawimg, contours, i, (0, 255, 0), 1)

    cv.imshow("shape number " + str(i), drawimg)
    if(len(contours) != 0):
        print(cv.contourArea(contours[i]) / scale * scale)

    key = cv.waitKeyEx(1)
    if key == ord('q'):
        break
    elif key == ord('i'):
        i = (i + 1) % len(contours)


cv.destroyAllWindows()


def next_element():
    if hierarchy[i][2] and hierarchy[hierarchy[i][2]][0] != -1:
        return hierarchy[i][2]
    elif hierarchy[i][0] != -1:
        return hierarchy[i][0]
    else:
        return hierarchy[i][3]
