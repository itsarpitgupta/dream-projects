from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class PixelCountInput(BaseInput):

    def __init__(self, main_ing, type, method, option, threshold, max_value, block_size, constant, next_tool):
        self.type = type
        self.main_img = main_ing
        self.method = method
        self.upper_threshold = threshold
        self.lower_threshold = max_value
        self.next_tool = next_tool
        self.option = option
        self.block_size = block_size
        self.constant = constant

    # default values
    type = ToolType.PIXEL_COUNT
    method = ["PIXEL_COUNT_METHOD_THRESH_BINARY"]
    option = Constant.PIXEL_COUNT_TOOL_ON_BINARY_THRESHOLD
    threshold = 124
    max_value = 255

    # for adaptive threshold
    # block size should be always be odd number
    block_size = 3
    constant = 8
