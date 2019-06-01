from com.deepvision.constants import Constant
from com.deepvision.output.BaseOutput import BaseOutput


class TextDetectionOutput(BaseOutput):
    status = Constant.TOOL_PASS
    box_lists = []
