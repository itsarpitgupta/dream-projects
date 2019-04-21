import ToolI
from BaseInput import BaseInput
from BaseOutput import BaseOutput
from ToolType import ToolType


class ToolEngine(object):
    toolList = [];

    def registerTool(tool: ToolI):
        toolList.append(tool);

    def applyTool(self, input: BaseInput) -> BaseOutput:

        for tool in toolList:
            if (input.type == ToolType.TEMPLATE_MATCHING):
                output = tool.proces(input)
            else:
                break;
                
        return output;
