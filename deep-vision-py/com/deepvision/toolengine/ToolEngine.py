from ToolI import ToolI
from BaseInput import BaseInput
from BaseOutput import BaseOutput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.constants.ToolType import ToolType
from typing import List


class ToolEngine(object):
    tool = None;

    def __init__(self):
        self.tool = ToolI();

    def registerTool(self, tool: ToolI):
        self.tool = tool;

    def applyTool(self, input: BaseInput) -> BaseOutput:
        output = BaseOutput();
        print(input.type)
        print(ToolType.TEMPLATE_MATCHING.value)
        if (input.type is ToolType.TEMPLATE_MATCHING.value):
            output = self.tool.process(input)
        if (input.type is ToolType.CORNER_DETECTION.value):
            output = self.tool.process(input)
        if (input.type is ToolType.EDGE_DETECTION.value):
            output = self.tool.process(input)
        if (input.type is ToolType.ANGLE_DETECTION.value):
            output = self.tool.process(input)
        else:
            output.status = ToolType.NO_TOOL
        return output;
