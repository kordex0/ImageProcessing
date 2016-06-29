
from glob import glob as gb
import cv2

def glob(patterns, ordered=False):
    if isinstance(patterns, list):
        if ordered:
            l = []
        else:
            s = set()
        for pattern in patterns:
            if pattern.startswith("!"):
                pattern = pattern[1:]
                fnames = glob(pattern)
                if ordered:
                    for fname in fnames:
                        if fname in l:
                            l.remove(fname)
                else:
                    s = s.difference(fnames)
            else:
                fnames = glob(pattern)
                if ordered:
                    for fname in fnames:
                        if fname not in l:
                            l.append(fname)
                else:
                    s = s.union(fnames)
        if ordered:
            return l
        else:
            return s
    else:
        return glob(patterns)

def cvimageiterator(patterns, ordered=False):
    fnames = filenames(patterns, ordered)
    for fname in fnames:
        yield cv2.imread(fname)

        
