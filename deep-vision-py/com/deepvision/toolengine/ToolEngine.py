from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.BaseInput import BaseInput
from com.deepvision.output.BaseOutput import BaseOutput
from com.deepvision.toolengine.ToolI import ToolI


class ToolEngine(object):
    tool = None;

    def __init__(self):
        self.tool = ToolI();

    def registerTool(self, tool: ToolI):
        self.tool = tool;

    def applyTool(self, input: BaseInput) -> BaseOutput:
        output = BaseOutput();
        # print(input.type)
        # print(ToolType.TEMPLATE_MATCHING.value)
        if (input.type == ToolType.TEMPLATE_MATCHING.value):
            output = self.tool.process(input)
        if (input.type == ToolType.CORNER_DETECTION.value):
            output = self.tool.process(input)
        if (input.type == ToolType.EDGE_DETECTION.value):
            output = self.tool.process(input)
        if (input.type == ToolType.ANGLE_DETECTION.value):
            output = self.tool.process(input)
        if (input.type == ToolType.DISTANCE_DETECTION.value):
            output = self.tool.process(input)
        else:
            output.status = ToolType.NO_TOOL
        return output;
