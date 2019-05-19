import cv2 as cv2
import matplotlib.pyplot as plt

from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.PixelCountInput import PixelCountInput
from com.deepvision.output.PixelCountOutput import PixelCountOutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import displayImageOutput


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

        count_white_px = cv2.countNonZero(thresh)
        count_black_px = thresh.shape[1] * thresh.shape[0] - count_white_px

        displayImageOutput(main_img=img, main_img_title="Main Img", result_img=thresh,
                           result_img_title=method, title="Adaptive Image Threshold")

        output.max_color_value = img.max()
        output.pixel_count = ret
        output.status = Constant.TOOL_PASS
        output.result_img = thresh
        output.non_zero_pixel_count = count_white_px
        output.zero_pixel_count = count_black_px
        return output

    def adaptiveImageThresholding(self, main_img, method, max_value, block_size, constant) -> PixelCountOutput:
        output = PixelCountOutput()
        img = cv2.imread(main_img, 0)

        thresh = cv2.adaptiveThreshold(img, max_value, eval(method[0]), eval(method[1]), block_size, constant)

        count_white_px = cv2.countNonZero(thresh)
        count_black_px = thresh.shape[1] * thresh.shape[0] - count_white_px

        displayImageOutput(main_img=img, main_img_title="Main Img", result_img=thresh,
                           result_img_title=method, title="Adaptive Image Threshold")

        output.max_color_value = img.max()
        output.status = Constant.TOOL_PASS
        output.result_img = thresh
        output.non_zero_pixel_count = count_white_px
        output.zero_pixel_count = count_black_px
        return output
