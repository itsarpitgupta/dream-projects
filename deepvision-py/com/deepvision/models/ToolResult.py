from com.deepvision.output.BaseOutput import BaseOutput


class ToolResult:

    def __init__(self, img_path, type, result, time, output, next_tool):
        self.type = type
        self.result = result
        self.time = time
        self.output = output
        self.next_tool = next_tool
        self.img_path = img_path

    img_path: str
    type: str
    result: str
    time: float
    output: BaseOutput
    next_tool: []
