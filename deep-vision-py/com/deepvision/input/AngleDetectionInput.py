from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class AngleDetectionInput(BaseInput):
    # defaults
    type = ToolType.ANGLE_DETECTION
    point_1 = None
    point_2 = None
