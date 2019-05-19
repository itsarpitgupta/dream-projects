import cv2
import matplotlib.pyplot as plt
import numpy as np


class ContourDetection(object):

    def __int__(self):
        print('In side contour detection...')

    def detectExternalInternalContour(self, main_img, type):
        # Check image is exist or not
        if main_img is None:
            print("Image not found");
            exit(0);

        # Reading the Image
        image_acc = cv2.imread(main_img, 0);

        # if image is not gray scale
        # imgray = cv2.cvtColor(image_acc, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(imgray, 127, 255, 0)

        image, contours, hierarchy = cv2.findContours(image_acc, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        # To draw all the contours in an image:
        external_contour = np.zeros(image.shape)
        for i in range(len(contours)):
            # for External contours
            if type == 'EXTERNAL' and hierarchy[0][i][3] == -1:
                cv2.drawContours(external_contour,contours,i,255,-1)
            elif type == 'INTERNAL' and  hierarchy[0][i][3] != -1:
                cv2.drawContours(external_contour, contours, i, 255, -1)

        plt.subplot(121), plt.imshow(image_acc, cmap='gray')
        plt.title('Main Image')  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(external_contour, cmap='gray')
        plt.title(type+' Contour')  # , plt.xticks([]), plt.yticks([])
        plt.suptitle('Contour Detection')
        plt.show()