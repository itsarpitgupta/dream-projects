from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class TextRecoginationInput(BaseInput):

    def __init__(self, type, box_lists, padding, next_tool):
        self.type = type
        self.box_lists = box_lists
        self.padding = padding
        self.next_tool = next_tool

    # default values
    type = ToolType.TEXT_RECOGINATION
    box_lists = []
    # amount of padding to add to each border of ROI
    padding = 0.0
