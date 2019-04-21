from ToolType import ToolType
from BaseInput import BaseInput


class TemplateMatchingInput(BaseInput):
    height = 0;
    width = 0;
    image = None;
    type = ToolType.TEMPLATE_MATCHING
