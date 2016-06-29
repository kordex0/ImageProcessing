
import cv2
import numpy as np
import sys

GRID_WIDTH = 9
GRID_HEIGHT = 6

REQUIRED_IMAGES = 9

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((GRID_WIDTH*GRID_HEIGHT, 3), np.float32)
objp[:,:2] = np.mgrid[0:GRID_WIDTH, 0:GRID_HEIGHT].T.reshape(-1,2)

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(0)

count = 0

_, img = cap.read()
h, w = img.shape[:2]

box_x = 0
box_y = 0
box_width = w/3
box_height = h/3

text_display = ""

while(True):
    _, img = cap.read()
    cv2.rectangle(img, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 0, 255), 2)
    disp = cv2.flip(img, 1);
    if text_display:
        cv2.putText(disp, text_display, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
    cv2.imshow('calibration', disp)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    if key & 0xFF == ord(' '):
        chessimg = img.copy()
        gray = cv2.cvtColor(chessimg, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (GRID_WIDTH, GRID_HEIGHT), None)
        if ret:
            cornersx = corners[:, 0, 0]
            cornersy = corners[:, 0, 1]
            if (cornersx > box_x).all() and (cornersx < box_x + box_width).all() and \
                    (cornersy > box_y).all() and (cornersy < box_y + box_height).all():
                text_display = ""
                count += 1
                box_y += box_height
                box_y %= h
                box_x += box_width if box_y == 0 else 0
                objpoints.append(objp)
                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)
                cv2.drawChessboardCorners(chessimg, (GRID_WIDTH, GRID_HEIGHT), corners, ret)
                cv2.imshow('img', chessimg)
            else:
                text_display = "Not inside Square"
        else:
            text_display = "Please try again"
    if count >= REQUIRED_IMAGES:
        break

if count >= REQUIRED_IMAGES:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    h, w = img.shape[:2]
    newcameratx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    while(True):
        _, img = cap.read()
        img = cv2.undistort(img, mtx, dist, None, newcameratx)
        disp = cv2.flip(img, 1);
        cv2.imshow('calibration', disp)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

