import cv2 as cv2
from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.CropInput import CropInput
from com.deepvision.output.CropOutput import CropOutput
from com.deepvision.toolengine.ToolI import ToolI
import matplotlib.pyplot as plt
import numpy as np


class CropTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.CROP

    def process(self, input: CropInput) -> CropOutput:
        if input.method == Constant.CROP_BY_POINT:
            output = self.cropByPoints(input.main_img, input.top_left, input.bottom_right)
        elif input.method == Constant.CROP_BY_PERCENTAGE:
            output = self.cropByPercentage(input.main_img, input.start_percentage, input.end_percentage)
        return output

    def cropByPoints(self, main_img, top_left, bottom_right) -> CropOutput:
        output = CropOutput()
        img = cv2.imread(main_img)

        x1, y1 = top_left[0], top_left[1]

        x2, y2 = bottom_right[0], bottom_right[1]

        cropped = img[y1:y2, x1:x2]

        # plt.subplot(121), plt.imshow(img, cmap='gray')
        # plt.title('Main Img')  # , plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(cropped, cmap='gray')
        # plt.title('Cropped Point')  # , plt.xticks([]), plt.yticks([])
        # plt.suptitle('Crop By Points')
        # plt.show()

        output.crop_image = cropped
        output.status = Constant.TOOL_PASS
        return output

    def cropByPercentage(self, main_img, start_percentage, end_percentage) -> CropOutput:
        output = CropOutput()
        img = cv2.imread(main_img)

        h, w = img.shape[:2]

        x1, y1 = int(h * start_percentage), int(w * start_percentage)

        x2, y2 = int(h * end_percentage), int(w * end_percentage)

        cropped = img[x1:x2, y1:y2]

        # plt.subplot(121), plt.imshow(img, cmap='gray')
        # plt.title('Main Img')  # , plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(cropped, cmap='gray')
        # plt.title('Cropped Point')  # , plt.xticks([]), plt.yticks([])
        # plt.suptitle('Crop By Points')
        # plt.show()

        output.crop_image = cropped
        output.status = Constant.TOOL_PASS

        return output
