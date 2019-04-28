from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from matplotlib import pyplot as plt

source_window = 'Source image'
corners_window = 'Corners detected'
max_thresh = 255


def cornerHarris_demo(val):
    thresh = val
    # Detector parameters
    blockSize = 2
    apertureSize = 3
    k = 0.04
    # Detecting corners
    dst = cv.cornerHarris(src_gray, blockSize, apertureSize, k)
    # Normalizing
    dst_norm = np.empty(dst.shape, dtype=np.float32)
    cv.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    dst_norm_scaled = cv.convertScaleAbs(dst_norm)
    # Drawing a circle around corners
    for i in range(dst_norm.shape[0]):
        for j in range(dst_norm.shape[1]):
            if int(dst_norm[i, j]) > thresh:
                cv.circle(dst_norm_scaled, (j, i), 5, (0), 2)
    # Showing the result
    cv.namedWindow(corners_window)
    cv.imshow(corners_window, dst_norm_scaled)


def shiTomasiAndGoodFeaturesToTrack(val):
    src_gray_cpy = np.copy(src_gray);
    corners = cv.goodFeaturesToTrack(src_gray_cpy, val, 0.01, 10)
    corners = np.int0(corners)


    # Drawing a circle around corners
    for i in corners:
        x, y = i.ravel()
        cv.circle(src_gray_cpy, (x, y), 3, (0 ,255, 0), -1)

    # Showing the result
    cv.namedWindow(corners_window)
    cv.imshow(corners_window, src_gray_cpy)


# Load source image and convert it to gray
parser = argparse.ArgumentParser(description='Code for Harris corner detector tutorial.')
parser.add_argument('--input', help='Path to input image.',
                    default='D:\github-repos\dream-projects\deep-vision-py\DATA\\flat_chessboard.png')
args = parser.parse_args()
# src = cv.imread(cv.samples.findFile(args.input))
src = cv.imread(args.input)
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# src_gray = cv.cvtColor(src, cv.COLOR_BGR2RGB)
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

# Create a window and a trackbar
cv.namedWindow(source_window)

# corner Harris demo
thresh = 100  # initial threshold
cv.createTrackbar('Threshold: ', source_window, thresh, max_thresh, cornerHarris_demo)
cv.imshow(source_window, src)
cornerHarris_demo(thresh)
cv.waitKey()


"""
# shi Tomasi And Good Features To Track
no_of_corner = 25  # initial corners
cv.createTrackbar('No of Corners', source_window, no_of_corner, max_thresh, shiTomasiAndGoodFeaturesToTrack)
cv.imshow(source_window, src)
shiTomasiAndGoodFeaturesToTrack(no_of_corner)
cv.waitKey()
"""