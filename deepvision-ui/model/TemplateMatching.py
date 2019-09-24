from model.Tool import Tool


class TemplateMatching(Tool):

    def __init__(self, main_img, temp_img, method, option, type, display, output, next_tool):
        Tool.__init__(self, type, display, output, next_tool)
        print("hello")
        self.main_img = main_img
        self.temp_img = temp_img
        self.method = method
        self.option = option
