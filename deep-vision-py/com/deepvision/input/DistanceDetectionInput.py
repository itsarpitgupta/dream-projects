from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class DistanceDetectionInput(BaseInput):
    # default values
    type = ToolType.DISTANCE_DETECTION
    method = Constant.DISTANCE_DETECTION_METHOD_PX

    point_1 = None
    point_2 = None