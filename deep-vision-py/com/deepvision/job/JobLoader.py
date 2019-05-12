import json as json
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.input.DistanceDetectionInput import DistanceDetectionInput
from com.deepvision.input.AngleDetectionInput import AngleDetectionInput
from com.deepvision.input.EdgeDetectionInput import EdgeDetectionInput


class JobLoader(object):
    tool_list = []
    jobJsonData = "";

    def loadJob(self):
        with open("..//job//job3.json", "r") as read_file:
            self.jobJsonData = json.load(read_file)

        print('Job Name : ' + self.jobJsonData['job_name'])
        print('Job Description : ' + self.jobJsonData['job_description'])
        print('Job Created By :' + self.jobJsonData['created_by'])
        tools = self.jobJsonData['tools']
        for tool in tools:
            tool_type = tool['type']
            if (ToolType.CORNER_DETECTION.value == tool_type):
                input = self.createCornerDetectionInput(tool)
            if (ToolType.TEMPLATE_MATCHING.value == tool_type):
                input = self.createTemplateMatchingInput(tool)
            if (ToolType.ANGLE_DETECTION.value == tool_type):
                input = self.createAngleDetectionInput(tool)
            if (ToolType.DISTANCE_DETECTION.value == tool_type):
                input = self.createDistanceDetectionInput(tool)
            if (ToolType.EDGE_DETECTION.value == tool_type):
                input = self.createEdgeDetectionInput(tool)
            self.tool_list.append(input);

    def createCornerDetectionInput(self, tool) -> CornerDetectionInput:
        input = CornerDetectionInput(tool['main_img'], tool['type'], tool['method'], tool['threshold'],
                                     tool['blockSize'],
                                     tool['apertureSize'], tool['k_size'],
                                     tool['max_thresholding'], tool['maxCorners'], tool['next_tool']);

        return input;

    def createTemplateMatchingInput(self, tool) -> TemplateMatchingInput:
        input = TemplateMatchingInput(tool['type'], tool['method'], tool['main_img'], tool['temp_img'], tool['option'],
                                      tool['next_tool'])
        return input

    def createAngleDetectionInput(self, tool) -> AngleDetectionInput:
        input = AngleDetectionInput(tool['type'], tool['point_1'], tool['point_2'], tool['next_tool'])
        return input

    def createDistanceDetectionInput(self, tool) -> DistanceDetectionInput:
        input = DistanceDetectionInput(tool['type'], tool['method'], tool['point_1'], tool['point_2'])
        return input

    def createEdgeDetectionInput(self, tool) -> EdgeDetectionInput:
        input = EdgeDetectionInput(tool['main_img'], tool['type'], tool['method'], tool['lower_threshold'],
                                   tool['upper_threshold'],
                                   tool['k_sizeX'], tool['k_sizeY'], tool['edge_thickness'], tool['next_tool'])
        return input
