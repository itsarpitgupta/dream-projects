from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class CornerDetectionInput(BaseInput):

    def __init__(self, main_img, type, method, threshold, blockSize, apertureSize, k_size, max_thresholding, maxCorners,
                 next_tool):
        self.main_img = main_img
        self.type = type
        self.method = method
        self.threshold = threshold
        self.blockSize = blockSize
        self.apertureSize = apertureSize
        self.k_size = k_size
        self.max_thresholding = max_thresholding
        self.maxCorners = maxCorners
        self.next_tool = next_tool

    # defaults
    type = ToolType.CORNER_DETECTION
    method = Constant.HARRIS_CORNER_DETECTION
    threshold = 100
    blockSize = 2
    apertureSize = 3
    k_size = 0.04
    max_thresholding = 100
    maxCorners = 5
    next_tool = None
