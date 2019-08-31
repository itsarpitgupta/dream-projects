from com.deepvision.output.BaseOutput import BaseOutput


class ToolResult:

    def __init__(self, type, result, time, output, next_tool):
        self.type = type
        self.result = result
        self.time = time
        self.output = output
        self.next_tool = next_tool

    type: str
    result: str
    time: float
    output: BaseOutput
    next_tool: []
