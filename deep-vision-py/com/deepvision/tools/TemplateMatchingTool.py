import cv2
import matplotlib.pyplot as plt
import numpy as np
from com.deepvision.constants import ToolType, Constant
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.output.TemplateMatchingOutput import TemplateMatchingOutput
from com.deepvision.toolengine.ToolI import ToolI


class TemplateMatchingTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.TEMPLATE_MATCHING

    def process(self, input: TemplateMatchingInput) -> TemplateMatchingOutput:
        output = TemplateMatchingOutput();
        if input.option == Constant.TEMPLATE_MATCHING_ON_SINGLE_OBJECT:
            output = self.matchTemplateWithSingleObject(input.main_img, input.temp_img, input.method)
        else:
            output = self.matchTemplateWithMultipleObject(input.main_img, input.temp_img)
        return output;

    def matchTemplateWithSingleObject(self, main_img, temp_img, opt) -> TemplateMatchingOutput:
        output = TemplateMatchingOutput();

        # reading the main image
        full_gray = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)

        # reading the template image
        template_gray = cv2.imread(temp_img, cv2.IMREAD_GRAYSCALE)

        # getting width, height and channels
        w, h = template_gray.shape[::-1]

        # create a copy of main image for operations
        img = full_gray.copy()
        method = eval(opt)

        # Apply template Matching
        res = cv2.matchTemplate(img, template_gray, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Apply thresholing
        threshold = 0.8
        if max_val >= threshold:
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            output.status = Constant.RESULT_MATCH_FOUND
            output.top_left_pnt = top_left
            output.bottom_right_pnt = bottom_right
        else:
            output.status = Constant.RESULT_NO_MATCH_FOUND

        plt.subplot(121), plt.imshow(template_gray, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(method)

        plt.show()

        return output

    def matchTemplateWithMultipleObject(self, main_img, temp_img) -> TemplateMatchingOutput:

        output = TemplateMatchingOutput()
        # reading the main image
        img_rgb = cv2.imread(main_img)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        # reading the template image
        template = cv2.imread(temp_img, 0)

        # getting width, height and channels
        w, h = template.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

        # Apply thresholing
        threshold = 0.8
        loc = np.where(res >= threshold)
        # print(res)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
            output.status = Constant.RESULT_MATCH_FOUND
        else:
            if output.status != Constant.RESULT_MATCH_FOUND:
                output.status = Constant.RESULT_NO_MATCH_FOUND

        plt.subplot(121), plt.imshow(template, cmap='gray')
        plt.title('Template Image')  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img_rgb, cmap='gray')
        plt.title('Detected Point')  # , plt.xticks([]), plt.yticks([])
        plt.suptitle('cv2.TM_CCOEFF_NORMED')

        plt.show()

        # cv2.imwrite('res.png', img_rgb)

        return output
