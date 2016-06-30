
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
    disp = cv2.flip(img, 1);
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

