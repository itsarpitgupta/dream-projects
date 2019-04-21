from ToolI import ToolI
from BaseInput import BaseInput
from BaseOutput import BaseOutput
from ToolType import ToolType
from typing import List


class ToolEngine(object):
    toolList = None;

    def __init__(self):
        self.toolList = [];

    def registerTool(self, tool: ToolI):
        self.toolList.append(tool)

    def applyTool(self, input: BaseInput) -> BaseOutput:

        for tool in self.toolList:
            if (input.type == ToolType.TEMPLATE_MATCHING):
                output = tool.process(input)
            else:
                break;

        return output;
