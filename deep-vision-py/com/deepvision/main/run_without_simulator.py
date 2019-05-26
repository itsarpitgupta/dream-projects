from com.deepvision.constants.ToolType import ToolType
from com.deepvision.job.JobLoader import JobLoader
from com.deepvision.toolengine.ToolEngine import ToolEngine
from com.deepvision.tools import FixtureTool
from com.deepvision.tools.AngleDetectionTool import AngleDetectionTool
from com.deepvision.tools.CornerDetectionTool import CornerDetectionTool
from com.deepvision.tools.CropTool import CropTool
from com.deepvision.tools.DistanceDetectionTool import DistanceDetectionTool
from com.deepvision.tools.EdgeDetectionTool import EdgeDetectionTool
from com.deepvision.tools.FixtureTool import FixtureTool
from com.deepvision.tools.PixelCountTool import PixelCountTool
from com.deepvision.tools.TemplateMatchingTool import TemplateMatchingTool


def main():

    toolEngine = ToolEngine()
    jobLoader = JobLoader()
    jobLoader.loadJob()
    outputList = []
    for tool in jobLoader.tool_list:
        print(tool.type + " : ")

        if (ToolType.CORNER_DETECTION.value == tool.type):
            toolEngine.registerTool(CornerDetectionTool())
        if (ToolType.TEMPLATE_MATCHING.value == tool.type):
            toolEngine.registerTool(TemplateMatchingTool())
        if (ToolType.ANGLE_DETECTION.value == tool.type):
            toolEngine.registerTool(AngleDetectionTool())
        if (ToolType.DISTANCE_DETECTION.value == tool.type):
            toolEngine.registerTool(DistanceDetectionTool())
        if (ToolType.EDGE_DETECTION.value == tool.type):
            toolEngine.registerTool(EdgeDetectionTool())
        if (ToolType.CROP.value == tool.type):
            toolEngine.registerTool(CropTool())
        if (ToolType.PIXEL_COUNT.value == tool.type):
            toolEngine.registerTool(PixelCountTool())
        if (ToolType.FIXTURE.value == tool.type):
            toolEngine.registerTool(FixtureTool())

        output = toolEngine.applyTool(tool)
        print(output.status)
        # print(output.top_left_pnt)
        # print(output.bottom_right_pnt)
        outputList.append(output)
        # Next tool execution
        next_tool = tool.next_tool
        i = 0
        while next_tool != None and len(next_tool) != 0:
            print(next_tool[i]['type'] + " : ")

            if (ToolType.CORNER_DETECTION.value == next_tool[i]['type']):
                toolEngine.registerTool(CornerDetectionTool())
                next_tool_input = jobLoader.createCornerDetectionInput(next_tool[i])
                next_tool_input.main_img = eval(next_tool[i]['main_img'])

            if (ToolType.TEMPLATE_MATCHING.value == next_tool[i]['type']):
                toolEngine.registerTool(TemplateMatchingTool())
                next_tool_input = jobLoader.createTemplateMatchingInput(next_tool[i])

            if (ToolType.ANGLE_DETECTION.value == next_tool[i]['type']):
                toolEngine.registerTool(AngleDetectionTool())
                next_tool_input = jobLoader.createAngleDetectionInput(next_tool[i])
                next_tool_input.point_1 = output.point_1
                next_tool_input.point_2 = output.point_2

            if (ToolType.DISTANCE_DETECTION.value == next_tool[i]['type']):
                toolEngine.registerTool(DistanceDetectionTool())
                next_tool_input = jobLoader.createDistanceDetectionInput(next_tool[i])
                next_tool_input.point_1 = eval(next_tool[i]['point_1'])
                next_tool_input.point_2 = eval(next_tool[i]['point_2'])

            if (ToolType.EDGE_DETECTION.value == next_tool[i]['type']):
                toolEngine.registerTool(EdgeDetectionTool())
                next_tool_input = jobLoader.createEdgeDetectionInput(next_tool[i])
                next_tool_input.main_img = eval(next_tool[i]['main_img'])

            if (ToolType.CROP.value == next_tool[i]['type']):
                toolEngine.registerTool(CropTool())
                next_tool_input = jobLoader.createCropInput(next_tool[i])
                next_tool_input.top_left = eval(next_tool[i]['top_left'])
                next_tool_input.bottom_right = eval(next_tool[i]['bottom_right'])

            if (ToolType.PIXEL_COUNT.value == next_tool[i]['type']):
                toolEngine.registerTool(PixelCountTool())
                next_tool_input = jobLoader.createPixelCountInput(next_tool[i])
                next_tool_input.main_img = eval(next_tool[i]['main_img'])

            if (ToolType.FIXTURE.value == next_tool[i]['type']):
                toolEngine.registerTool(FixtureTool())
                next_tool_input = jobLoader.createFixtureInput(next_tool[i])
                next_tool_input.top_left_pnt = eval(next_tool[i]['top_left_pnt'])
                next_tool_input.bottom_right_pnt = eval(next_tool[i]['bottom_right_pnt'])

            output = toolEngine.applyTool(next_tool_input)
            print(output.status)
            # print(output.next_top_left_pnt)
            # print(output.next_bottom_right_pnt)
            outputList.append(output)
            next_tool = next_tool[i]['next_tool']


if __name__ == "__main__":
    main();
