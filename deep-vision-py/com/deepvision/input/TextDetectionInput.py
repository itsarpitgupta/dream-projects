from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class TextDetectionInput(BaseInput):

    def __init__(self, type, threshold, width, height, next_tool):
        self.type = type
        self.threshold = threshold
        self.width = width
        self.height = height
        self.next_tool = next_tool

    # default values
    type = ToolType.TEXT_DETECTION
    # minimum probability required to inspect a region
    threshold = 0.5
    # resized image width (should be multiple of 32)
    width = 320
    # resized image height (should be multiple of 32)
    height = 320
