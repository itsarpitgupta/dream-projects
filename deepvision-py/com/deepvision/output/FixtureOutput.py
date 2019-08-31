from com.deepvision.constants import Constant
from com.deepvision.output.BaseOutput import BaseOutput


class FixtureOutput(BaseOutput):
    status = Constant.TOOL_PASS
    next_top_left_pnt = []
    next_bottom_right_pnt = []
