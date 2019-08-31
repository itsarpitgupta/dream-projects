from com.deepvision.constants import ToolType, Constant
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.DistanceDetectionInput import DistanceDetectionInput
from com.deepvision.output.DistanceDetectionOutput import DistanceDetectionOutput
from com.deepvision.toolengine.ToolI import ToolI
from scipy.spatial import distance as dist


class DistanceDetectionTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.ToolType.DISTANCE_DETECTION

    def process(self, input: DistanceDetectionInput) -> DistanceDetectionOutput:
        output = self.distanceDetection(input.method, input.point_1, input.point_2)
        return output;

    def distanceDetection(self, method, point_1, point_2) -> DistanceDetectionOutput:
        output = DistanceDetectionOutput()
        try:
            # validate the points
            if point_1 is None or point_2 is None:
                raise DataValidationException("Point1 or Point2 should not be None")

            output.total_distance = dist.euclidean(point_1, point_2)
            output.status = Constant.TOOL_PASS
        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
