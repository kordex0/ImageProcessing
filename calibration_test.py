import numpy as np
import cv2
import glob

from utils.fileutils import cvimageiterator

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*7, 3), np.float32)
objp[:,:2] = np.mgrid[0:7, 0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

images = glob.glob('left*.jpg')

for img in cvimageiterator('left*.jpg'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
    
    if ret:
        objpoints.append(objp)
        
        cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        
        cv2.drawChessboardCorners(img, (7, 6), corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

for img in cvimageiterator('left*.jpg'):
    img = cv2.imread(fname)
    h, w = img.shape[:2]
    newcameratx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newcameratx)
    cv2.imshow('img', dst)
    cv2.waitKey(500)

mean_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
    
print "total error: ", mean_error/len(objpoints)

cv2.destroyAllWindows()

