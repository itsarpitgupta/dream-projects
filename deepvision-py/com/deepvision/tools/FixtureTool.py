from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.FixtureInput import FixtureInput
from com.deepvision.output import FixtureOutput
from com.deepvision.output.FixtureOutput import FixtureOutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import draw_multiple_points, draw_single_point


class FixtureTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.FIXTURE

    def process(self, input: FixtureInput) -> FixtureOutput:
        return self.findFixturePnt(input.top_left_pnt, input.bottom_right_pnt, input.top_left_pnt_gape,
                                   input.bottom_right_pnt_gape)

    def findFixturePnt(self, top_left_pnt, bottom_right_pnt, top_left_pnt_gape, bottom_right_pnt_gape) -> FixtureOutput:
        output = FixtureOutput()
        try:
            if top_left_pnt is None or bottom_right_pnt is None or top_left_pnt_gape is None or bottom_right_pnt_gape is None:
                raise DataValidationException(
                    'top_left_pnt, bottom_right_pnt, top_left_pnt_gape or bottom_right_pnt should not be none')

            if self.display:
                draw_multiple_points(x_number_list=[top_left_pnt[0], bottom_right_pnt[0]],
                                     y_number_list=[top_left_pnt[1], bottom_right_pnt[1]],
                                     title="Template matching points")

            next_top_left_pnt = [top_left_pnt_gape[0] + top_left_pnt[0], top_left_pnt_gape[1] + top_left_pnt[1]]
            next_bottom_right_pnt = [bottom_right_pnt_gape[0] + bottom_right_pnt[0],
                                     bottom_right_pnt_gape[1] + bottom_right_pnt[1]]

            if self.display:
                draw_multiple_points(x_number_list=[next_top_left_pnt[0], next_bottom_right_pnt[0]],
                                     y_number_list=[next_top_left_pnt[1],
                                                    next_bottom_right_pnt[1]], title="Fixture points")

            output.status = Constant.TOOL_PASS
            output.next_top_left_pnt = next_top_left_pnt
            output.next_bottom_right_pnt = next_bottom_right_pnt

        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
