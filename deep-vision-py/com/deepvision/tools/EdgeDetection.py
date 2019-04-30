from __future__ import print_function
import cv2
import numpy as np
import argparse
from matplotlib import pyplot as plt

source_window = 'Source image'
edge_window = 'Edge detected'
max_thresh = 400
# corner Harris demo
lower = 100  # initial threshold
upper = 200  # initial threshold
ksizX = 5  # initial threshold
ksizeY = 5  # initial threshold

def doNothing(self):
    pass

def cannyEdgeDetection(lower,upper,ksizX,ksizeY):
    # img = cv2.imread(src_gray, 0)

    # LOWER THRESHOLD TO EITHER 0 OR 70% OF THE MEDIAN VALUE WHICH EVER IS GREATER
    # lower = int(max(0, 0.7 * np.median(img)))
    # UPPER THRESHOLD TO EITHER 130% OF THE MEDIAN VALUE OF THE 255, WHICH EVER IS SMALLER
    # upper = int(min(255, 1.3 * np.median(img)))

    blurred_img = cv2.blur(src_gray, ksize=(ksizX, ksizeY))

    edges = cv2.Canny(blurred_img, threshold1=lower, threshold2=upper)

    """
    plt.subplot(121), plt.imshow(img, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()
    """

    # Showing the result
    cv2.namedWindow(edge_window)
    cv2.imshow(edge_window, edges)


# Load source image and convert it to gray
parser = argparse.ArgumentParser(description='Code for Harris corner detector tutorial.')
parser.add_argument('--input', help='Path to input image.',
                    default='D:\github-repos\dream-projects\deep-vision-py\DATA\\Image00111.BMP')
args = parser.parse_args()
# src = cv2.imread(cv2.samples.findFile(args.input))
src = cv2.imread(args.input)
if src is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# src_gray = cv.cvtColor(src, cv.COLOR_BGR2RGB)
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# Create a window and a trackbar
cv2.namedWindow(source_window)

cv2.createTrackbar('Threshold1', source_window, lower, max_thresh, doNothing)
cv2.createTrackbar('Threshold2', source_window, upper, max_thresh, doNothing)
cv2.createTrackbar('KsizeX', source_window, ksizX, 10, doNothing)
cv2.createTrackbar('KsizeY', source_window, ksizeY, 10, doNothing)


while(1):
    cv2.imshow(source_window, src)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    lower = cv2.getTrackbarPos('Threshold1',source_window)
    upper = cv2.getTrackbarPos('Threshold2',source_window)
    ksizX = cv2.getTrackbarPos('KsizeX',source_window)
    ksizeY = cv2.getTrackbarPos('KsizeY',source_window)

    cannyEdgeDetection(lower,upper,ksizX,ksizeY)

cv2.waitKey()
cv2.destroyAllWindows()
