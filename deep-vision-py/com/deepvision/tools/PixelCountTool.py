import cv2 as cv2
import matplotlib.pyplot as plt

from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.PixelCountInput import PixelCountInput
from com.deepvision.output.PixelCountOutput import PixelCountOutput
from com.deepvision.toolengine.ToolI import ToolI


class PixelCountTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.PIXEL_COUNT

    def process(self, input: PixelCountInput) -> PixelCountOutput:
        if input.option == Constant.PIXEL_COUNT_TOOL_ON_BINARY_THRESHOLD:
            return self.binaryImageThresholding(input.main_img, input.method, input.threshold, input.max_value)
        elif input.option == Constant.PIXEL_COUNT_TOOL_ON_ADAPTIVE_THRESHOLD:
            return self.adaptiveImageThresholding(input.main_img, input.method, input.max_value, input.block_size,
                                                  input.constant)

    def binaryImageThresholding(self, main_img, method, threshold, max_value) -> PixelCountOutput:
        output = PixelCountOutput()
        img = cv2.imread(main_img, 0)
        ret, thresh = cv2.threshold(img, threshold, max_value, eval(method[0]))
        print(ret)
        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Main Img')  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(thresh, cmap='gray')
        plt.title(method)  # , plt.xticks([]), plt.yticks([])
        plt.suptitle('Binary Image Threshold')
        plt.show()

        output.max_color_value = img.max()
        output.pixel_count = ret
        output.status = Constant.TOOL_PASS
        output.result_img = thresh
        output.non_zero_pixel_count = cv2.countNonZero(thresh)
        return output

    def adaptiveImageThresholding(self, main_img, method, max_value, block_size, constant) -> PixelCountOutput:
        output = PixelCountOutput()
        img = cv2.imread(main_img, 0)

        thresh = cv2.adaptiveThreshold(img, max_value, eval(method[0]), eval(method[1]), block_size, constant)


        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Main Img')  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(thresh, cmap='gray')
        plt.title(method)  # , plt.xticks([]), plt.yticks([])
        plt.suptitle('Adaptive Image Threshold')
        plt.show()

        output.max_color_value = img.max()
        output.status = Constant.TOOL_PASS
        output.result_img = thresh
        output.non_zero_pixel_count = cv2.countNonZero(thresh)
        return output
