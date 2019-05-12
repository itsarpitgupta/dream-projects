from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class DistanceDetectionInput(BaseInput):

    def __init__(self, type, method, point_1, point_2):
        self.type = type
        self.point_1 = point_1
        self.point_2 = point_2
        self.method = method

    # default values
    type = ToolType.DISTANCE_DETECTION
    method = Constant.DISTANCE_DETECTION_METHOD_PX

    point_1 = []
    point_2 = []
