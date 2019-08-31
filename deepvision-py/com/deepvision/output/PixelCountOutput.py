from com.deepvision.constants import Constant
from com.deepvision.output.BaseOutput import BaseOutput


class PixelCountOutput(BaseOutput):
    status = Constant.TOOL_PASS
    non_zero_pixel_count = 0
    zero_pixel_count = 0
    max_color_value = 0
    result_img = []
