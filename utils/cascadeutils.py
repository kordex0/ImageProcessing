
import cv2

from os import path

DEFAULT_LOCATION = "~/Documents/Workspace/ImageProcessing/cascades"
SYSTEM_LOCATION = "~/Documents/Workspace/opencv/data/haarcascades"

def get_cascade(name):
    default_path = path.expanduser(path.join(DEFAULT_LOCATION, name))
    system_path = path.expanduser(path.join(SYSTEM_LOCATION, name))
    if path.exists(default_path):
        return cv2.CascadeClassifier(default_path)
    elif path.exists(system_path):
        return cv2.CascadeClassifier(system_path)
    else:
        return None

