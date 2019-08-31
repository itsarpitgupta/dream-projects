from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput


class FixtureInput(BaseInput):

    def __init__(self, type, top_left_pnt, bottom_right_pnt, top_left_pnt_gape, bottom_right_pnt_gape, next_tool):
        self.type = type
        self.next_tool = next_tool
        self.top_left_pnt = top_left_pnt
        self.bottom_right_pnt = bottom_right_pnt
        self.top_left_pnt_gape = top_left_pnt_gape
        self.bottom_right_pnt_gape = bottom_right_pnt_gape

    # default values
    type = ToolType.FIXTURE
    top_left_pnt = []
    bottom_right_pnt = []

    top_left_pnt_gape = []
    bottom_right_pnt_gape = []
