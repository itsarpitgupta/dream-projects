import cv2
import numpy as np
import matplotlib.pyplot as plt

# %matplotlib inline

class TemplateMatching(object):

    def __int__(self):
        print("in template constructor");


    def matchTemplateWithSingleObject(main_img, temp_img, method):
        full = cv2.imread('E:\OpenCV and Python\code\DATA\sammy.jpg')
        full = cv2.cvtColor(full, cv2.COLOR_BGR2RGB)

        # plt.imshow(full)

        template = cv2.imread('E:\OpenCV and Python\code\DATA\sammy_face.jpg')
        template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
        w, h, c = template.shape

        # plt.imshow(template)

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF',
                   'cv2.TM_SQDIFF_NORMED']

        for meth in methods:
            img = full.copy()
            method = eval(meth)

            # Apply template Matching
            res = cv2.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            cv2.rectangle(img, top_left, bottom_right, 255, 2)

            plt.subplot(121), plt.imshow(res, cmap='gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(img, cmap='gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)

            plt.show()

    def matchTemplateWithMultipleObject(main_img, temp_img, method):
        img_rgb = cv2.imread('mario.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('mario_coin.png', 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite('res.png', img_rgb)