from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class EdgeDetectionInput(BaseInput):

    def __init__(self, type, method, lower_threshold, upper_threshold, k_sizeX, k_sizeY, edge_thickness):
        self.type = type
        self.method = method
        self.lower_threshold = lower_threshold
        self.upper_threshold = upper_threshold
        self.k_sizeY = k_sizeY
        self.k_sizeX = k_sizeX
        self.edge_thickness = edge_thickness

    # default values
    type = ToolType.EDGE_DETECTION
    method = Constant.CANNY_EDGE_DETECTION
    lower_threshold = 100
    upper_threshold = 200
    k_sizeX = 2
    k_sizeY = 3
    edge_thickness = 1;
