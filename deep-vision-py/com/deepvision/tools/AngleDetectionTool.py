import math

from com.deepvision.constants import ToolType, Constant
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
        angle = int(math.atan((point_1[1] - point_2[1]) / (point_2[0] - point_1[0])) * 180 / math.pi)
        output.angle_value = angle
        output.status = Constant.RESULT_MATCH_FOUND
        return output;
