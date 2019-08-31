from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class OCRInput(BaseInput):

    def __init__(self,main_img ,type, min_counter_area, text, next_tool):
        self.type = type
        self.min_counter_area = min_counter_area
        self.text = text
        self.main_img = main_img
        self.next_tool = next_tool

    # defaults
    type = ToolType.OCR
    min_counter_area = 30
    text = ''
    next_tool = None
