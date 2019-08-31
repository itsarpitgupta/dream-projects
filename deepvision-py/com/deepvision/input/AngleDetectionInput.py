from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class AngleDetectionInput(BaseInput):

    def __init__(self, type, point_1, point_2):
        self.type = type
        self.point_1 = point_1
        self.point_2 = point_2

    # defaults
    type = ToolType.ANGLE_DETECTION
    point_1 = None
    point_2 = None
