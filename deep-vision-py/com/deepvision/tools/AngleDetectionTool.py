import math

from com.deepvision.constants import ToolType, Constant
from com.deepvision.exception.BusinessException import BusinessException
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.AngleDetectionInput import AngleDetectionInput
from com.deepvision.output.AngleDetectionOutput import AngleDetectionOutput
from com.deepvision.toolengine.ToolI import ToolI


class AngleDetectionTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.ANGLE_DETECTION

    def process(self, input: AngleDetectionInput) -> AngleDetectionOutput:
        return self.angleDetection(input.point_1, input.point_2)

    def angleDetection(self, point_1, point_2) -> AngleDetectionOutput:
        output = AngleDetectionOutput()
        try:
            # validate the points
            if point_1 is None or point_2 is None:
                raise DataValidationException("Point1 or Point2 should not be None")

            angle = int(math.atan((point_1[1] - point_2[1]) / (point_2[0] - point_1[0])) * 180 / math.pi)
            output.angle_value = angle
            output.status = Constant.TOOL_PASS
        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
