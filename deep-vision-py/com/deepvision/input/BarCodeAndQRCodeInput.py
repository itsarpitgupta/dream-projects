from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class BarCodeAndQRCodeInput(BaseInput):

    def __init__(self, type, main_img, next_tool):
        self.type = type
        self.next_tool = next_tool
        self.main_img = main_img
        self.next_tool = next_tool

    # default values
    type = ToolType.BAR_CODE_AND_QR_CODE
    next_tool = None
