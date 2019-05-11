from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class TemplateMatchingInput(BaseInput):

    def __int__(self, type, method, main_img, temp_img, option):
        self.type = type
        self.method = method
        self.main_img = main_img
        self.temp_img = temp_img
        self.option = option

    type = ToolType.TEMPLATE_MATCHING
    main_img = None;
    temp_img = None;
    method = Constant.TEMPLATE_MATCHING_METHOD_TM_CCOEFF
    option = Constant.TEMPLATE_MATCHING_ON_SINGLE_OBJECT
