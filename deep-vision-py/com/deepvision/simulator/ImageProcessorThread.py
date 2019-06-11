import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
import cv2 as cv2
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.job.JobLoader import JobLoader
from com.deepvision.models.ToolResult import ToolResult
from com.deepvision.toolengine.ToolEngine import ToolEngine
from com.deepvision.tools import FixtureTool
from com.deepvision.tools.AngleDetectionTool import AngleDetectionTool
from com.deepvision.tools.BarCodeAndQRCodeReaderTool import BarCodeAndQRCodeReaderTool
from com.deepvision.tools.CornerDetectionTool import CornerDetectionTool
from com.deepvision.tools.CropTool import CropTool
from com.deepvision.tools.DistanceDetectionTool import DistanceDetectionTool
from com.deepvision.tools.EdgeDetectionTool import EdgeDetectionTool
from com.deepvision.tools.FixtureTool import FixtureTool
from com.deepvision.tools.OCRTool import OCRTool
from com.deepvision.tools.PixelCountTool import PixelCountTool
from com.deepvision.tools.TemplateMatchingTool import TemplateMatchingTool
from com.deepvision.tools.TextDetectionTool import TextDetectionTool
from com.deepvision.tools.TextRecoginationTool import TextRecoginationTool


class ImageProcessorThread(threading.Thread):
    main_img = []

    def __init__(self, name, image_process_queue, image_result_queue, tools, result_dict, job_loader):
        threading.Thread.__init__(self)
        self.name = name
        self.image_process_queue = image_process_queue
        self.image_result_queue = image_result_queue
        self.tools = tools
        self.result_dict = result_dict
        # self.job_loader = job_loader

    def run(self):
        self.process_image()

    def process_image(self):
        while True:
            # time.sleep(.5)
            img_path = self.image_process_queue.get()
            print(img_path)
            main_img = cv2.imread(img_path)

            # check if the load is high or not
            if self.image_process_queue.qsize() > 0:
                print('Load is high.')

            # results = []
            for tool in self.tools:
                tool.main_img = main_img
            #     result = process_tool(tool)
            #     results.append(result)

            # self.image_result_queue.put(list(results))

            start = time.time()
            with ThreadPoolExecutor(max_workers=5) as executor:
                results = executor.map(process_tool, self.tools)
            end = time.time()

            # put all the results from all the processor thread in result queue
            self.image_result_queue.put(list(results))


            print('__________________________________________________\n')
            print('Total time taken - {:.4f}\n'.format(end - start))


def process_tool(tool) -> ToolResult:
    toolEngine = ToolEngine()
    outputList = []
    job_loader = JobLoader()
    main_tool_start = time.time()
    if (ToolType.CORNER_DETECTION.value == tool.type):
        toolEngine.registerTool(CornerDetectionTool())
    elif (ToolType.TEMPLATE_MATCHING.value == tool.type):
        toolEngine.registerTool(TemplateMatchingTool())
    elif (ToolType.ANGLE_DETECTION.value == tool.type):
        toolEngine.registerTool(AngleDetectionTool())
    elif (ToolType.DISTANCE_DETECTION.value == tool.type):
        toolEngine.registerTool(DistanceDetectionTool())
    elif (ToolType.EDGE_DETECTION.value == tool.type):
        toolEngine.registerTool(EdgeDetectionTool())
    elif (ToolType.CROP.value == tool.type):
        toolEngine.registerTool(CropTool())
    elif (ToolType.PIXEL_COUNT.value == tool.type):
        toolEngine.registerTool(PixelCountTool())
    elif (ToolType.FIXTURE.value == tool.type):
        toolEngine.registerTool(FixtureTool())
    elif (ToolType.TEXT_DETECTION.value == tool.type):
        toolEngine.registerTool(TextDetectionTool())
    elif (ToolType.TEXT_RECOGINATION.value == tool.type):
        toolEngine.registerTool(TextRecoginationTool())
    elif (ToolType.OCR.value == tool.type):
        toolEngine.registerTool(OCRTool())
    elif (ToolType.BAR_CODE_AND_QR_CODE.value == tool.type):
        toolEngine.registerTool(BarCodeAndQRCodeReaderTool())

    output = toolEngine.applyTool(tool)
    outputList.append(output)
    main_tool_end = time.time()
    tool_result = ToolResult(type=tool.type, result=output.status,
                             time=(main_tool_end - main_tool_start), output=output, next_tool=[])

    # Next tool execution
    next_tool = tool.next_tool
    i = 0
    while next_tool != None and len(next_tool) != 0:
        next_tool_start = time.time()

        if (ToolType.CORNER_DETECTION.value == next_tool[i]['type']):
            toolEngine.registerTool(CornerDetectionTool())
            next_tool_input = job_loader.createCornerDetectionInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.TEMPLATE_MATCHING.value == next_tool[i]['type']):
            toolEngine.registerTool(TemplateMatchingTool())
            next_tool_input = job_loader.createTemplateMatchingInput(next_tool[i])

        elif (ToolType.ANGLE_DETECTION.value == next_tool[i]['type']):
            toolEngine.registerTool(AngleDetectionTool())
            next_tool_input = job_loader.createAngleDetectionInput(next_tool[i])
            next_tool_input.point_1 = output.point_1
            next_tool_input.point_2 = output.point_2

        elif (ToolType.DISTANCE_DETECTION.value == next_tool[i]['type']):
            toolEngine.registerTool(DistanceDetectionTool())
            next_tool_input = job_loader.createDistanceDetectionInput(next_tool[i])
            next_tool_input.point_1 = eval(next_tool[i]['point_1'])
            next_tool_input.point_2 = eval(next_tool[i]['point_2'])

        elif (ToolType.EDGE_DETECTION.value == next_tool[i]['type']):
            toolEngine.registerTool(EdgeDetectionTool())
            next_tool_input = job_loader.createEdgeDetectionInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.CROP.value == next_tool[i]['type']):
            toolEngine.registerTool(CropTool())
            next_tool_input = job_loader.createCropInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])
            next_tool_input.top_left = eval(next_tool[i]['top_left'])
            next_tool_input.bottom_right = eval(next_tool[i]['bottom_right'])

        elif (ToolType.PIXEL_COUNT.value == next_tool[i]['type']):
            toolEngine.registerTool(PixelCountTool())
            next_tool_input = job_loader.createPixelCountInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.FIXTURE.value == next_tool[i]['type']):
            toolEngine.registerTool(FixtureTool())
            next_tool_input = job_loader.createFixtureInput(next_tool[i])
            next_tool_input.top_left_pnt = eval(next_tool[i]['top_left_pnt'])
            next_tool_input.bottom_right_pnt = eval(next_tool[i]['bottom_right_pnt'])

        elif (ToolType.TEXT_DETECTION.value == next_tool[i]['type']):
            toolEngine.registerTool(TextDetectionTool())
            next_tool_input = job_loader.createTextDetectionInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.TEXT_RECOGINATION.value == next_tool[i]['type']):
            toolEngine.registerTool(TextRecoginationTool())
            next_tool_input = job_loader.createTextRecoginationInput(next_tool[i])
            next_tool_input.box_lists = eval(next_tool[i]['box_lists'])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.OCR.value == next_tool[i]['type']):
            toolEngine.registerTool(OCRTool())
            next_tool_input = job_loader.createOCRInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        elif (ToolType.BAR_CODE_AND_QR_CODE.value == next_tool[i]['type']):
            toolEngine.registerTool(BarCodeAndQRCodeReaderTool())
            next_tool_input = job_loader.createOCRInput(next_tool[i])
            next_tool_input.main_img = eval(next_tool[i]['main_img'])

        output = toolEngine.applyTool(next_tool_input)
        outputList.append(output)
        next_tool_end = time.time()
        next_tool_result = ToolResult(type=next_tool[i]['type'], result=output.status,
                                      time=(next_tool_end - next_tool_start), output=output, next_tool=[])

        tool_result.next_tool.append(next_tool_result)

        next_tool = next_tool[i]['next_tool']

    return tool_result
