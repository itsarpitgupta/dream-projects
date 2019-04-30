from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class EdgeDetectionInput(BaseInput):
    type = ToolType.EDGE_DETECTION
    method = Constant.CANNY_EDGE_DETECTION
    lower_threshold = 100
    upper_threshold = 200
    k_sizeX = 2
    k_sizeY = 3
