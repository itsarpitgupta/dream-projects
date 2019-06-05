import json as json

from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.AngleDetectionInput import AngleDetectionInput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.input.CropInput import CropInput
from com.deepvision.input.DistanceDetectionInput import DistanceDetectionInput
from com.deepvision.input.EdgeDetectionInput import EdgeDetectionInput
from com.deepvision.input.FixtureInput import FixtureInput
from com.deepvision.input.OCRInput import OCRInput
from com.deepvision.input.PixelCountInput import PixelCountInput
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.input.TextDetectionInput import TextDetectionInput
from com.deepvision.input.TextRecoginationInput import TextRecoginationInput
from com.deepvision.job.Job import Job


class JobLoader(object):
    tool_list = []
    jobJsonData = ""
    job = None
    result_dict = {}

    def loadJob(self):
        with open("..//job//json//job13.json", "r") as read_file:
            self.jobJsonData = json.load(read_file)

        # print('Job Name : ' + self.jobJsonData['job_name'])
        # print('Job Description : ' + self.jobJsonData['job_description'])
        # print('Job Created By :' + self.jobJsonData['created_by'])
        self.job = Job(self.jobJsonData['job_name'], self.jobJsonData['job_description'], self.jobJsonData['created_by']
                       , self.jobJsonData['created_date_time'], self.jobJsonData['modified_by'],
                       self.jobJsonData['modified_date_time'],
                       self.jobJsonData['tools'], self.jobJsonData['display'])

        for tool in self.job.tools:
            tool_type = tool['type']

            if (ToolType.CORNER_DETECTION.value == tool_type):
                input = self.createCornerDetectionInput(tool)
            elif (ToolType.TEMPLATE_MATCHING.value == tool_type):
                input = self.createTemplateMatchingInput(tool)
            elif (ToolType.ANGLE_DETECTION.value == tool_type):
                input = self.createAngleDetectionInput(tool)
            elif (ToolType.DISTANCE_DETECTION.value == tool_type):
                input = self.createDistanceDetectionInput(tool)
            elif (ToolType.EDGE_DETECTION.value == tool_type):
                input = self.createEdgeDetectionInput(tool)
            elif (ToolType.PIXEL_COUNT.value == tool_type):
                input = self.createPixelCountInput(tool)
            elif (ToolType.FIXTURE.value == tool_type):
                input = self.createFixtureInput(tool)
            elif (ToolType.TEXT_DETECTION.value == tool_type):
                input = self.createTextDetectionInput(tool)
            elif (ToolType.TEXT_RECOGINATION.value == tool_type):
                input = self.createTextRecoginationInput(tool)
            elif (ToolType.CROP.value == tool_type):
                input = self.createCropInput(tool)
            elif (ToolType.OCR.value == tool_type):
                input = self.createOCRInput(tool)
            self.tool_list.append(input)

    def createOCRInput(self, tool) -> OCRInput:
        input = OCRInput(tool['main_img'], tool['type'], tool['min_counter_area'], tool['text'])

        self.set_display(input, tool)
        return input

    def createCornerDetectionInput(self, tool) -> CornerDetectionInput:
        input = CornerDetectionInput(tool['main_img'], tool['type'], tool['method'], tool['threshold'],
                                     tool['blockSize'],
                                     tool['apertureSize'], tool['k_size'],
                                     tool['max_thresholding'], tool['maxCorners'], tool['next_tool'])

        self.set_display(input, tool)
        return input

    def createTemplateMatchingInput(self, tool) -> TemplateMatchingInput:
        input = TemplateMatchingInput(tool['type'], tool['method'], tool['main_img'], tool['temp_img'], tool['option'],
                                      tool['next_tool'])

        self.set_display(input, tool)
        return input

    def createAngleDetectionInput(self, tool) -> AngleDetectionInput:
        input = AngleDetectionInput(tool['type'], tool['point_1'], tool['point_2'], tool['next_tool'])

        self.set_display(input, tool)
        return input

    def createDistanceDetectionInput(self, tool) -> DistanceDetectionInput:
        input = DistanceDetectionInput(tool['type'], tool['method'], tool['point_1'], tool['point_2'])

        self.set_display(input, tool)

        return input

    def createEdgeDetectionInput(self, tool) -> EdgeDetectionInput:
        input = EdgeDetectionInput(tool['main_img'], tool['type'], tool['method'], tool['lower_threshold'],
                                   tool['upper_threshold'],
                                   tool['k_sizeX'], tool['k_sizeY'], tool['edge_thickness'], tool['next_tool'])

        self.set_display(input, tool)

        return input

    def createCropInput(self, tool) -> CropInput:
        input = CropInput(tool['main_img'], tool['type'], tool['method'], tool['top_left'],
                          tool['bottom_right'],
                          tool['start_percentage'], tool['end_percentage'], tool['next_tool'])

        self.set_display(input, tool)

        return input

    def createPixelCountInput(self, tool) -> PixelCountInput:
        input = PixelCountInput(tool['main_img'], tool['type'], tool['method'], tool['option'], tool['threshold'],
                                tool['max_value'], tool['block_size'], tool['constant'], tool['next_tool'])

        self.set_display(input, tool)

        return input

    def createFixtureInput(self, tool):
        input = FixtureInput(tool['type'], tool['top_left_pnt'], tool['bottom_right_pnt'], tool['top_left_pnt_gape'],
                             tool['bottom_right_pnt_gape'], tool['next_tool'])

        self.set_display(input, tool)

        return input

    def createTextDetectionInput(self, tool):
        input = TextDetectionInput(tool['type'], tool['threshold'], tool['width'], tool['height'], tool['next_tool'])

        self.set_display(input, tool)

        return input

    def set_display(self, input, tool):
        if self.job is not None and self.job.display == 'ON':
            input.display = True
        else:
            if tool['display'] == 'ON':
                input.display = tool['display']

    def createTextRecoginationInput(self, tool):
        input = TextRecoginationInput(tool['type'], tool['box_lists'], tool['padding'], tool['next_tool'])

        self.set_display(input, tool)

        return input
