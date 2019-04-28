from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.constants import Constant


class TemplateMatchingInput(BaseInput):
    type = ToolType.TEMPLATE_MATCHING
    main_img = None;
    temp_img = None;
    method = Constant.TEMPLATE_MATCHING_METHOD_TM_CCOEFF
    option = Constant.TEMPLATE_MATCHING_ON_SINGLE_OBJECT
