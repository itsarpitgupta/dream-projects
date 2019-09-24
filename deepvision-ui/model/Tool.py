class Tool(object):
    type = ""
    display = "OFF"
    output = []
    next_tool = []

    def __init__(self, type, display, output, next_tool):
        self.type = type
        self.display = display
        self.output = output
        self.next_tool = next_tool
