from com.deepvision.constants.ToolType import ToolType
from com.deepvision.job.JobLoader import JobLoader
from com.deepvision.toolengine.ToolEngine import ToolEngine
from com.deepvision.tools.TemplateMatchingTool import TemplateMatchingTool
from com.deepvision.tools.CornerDetectionTool import CornerDetectionTool
from com.deepvision.tools.DistanceDetectionTool import DistanceDetectionTool
from com.deepvision.tools.EdgeDetectionTool import EdgeDetectionTool
from com.deepvision.input.EdgeDetectionInput import EdgeDetectionInput
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.output.CornerDetectionOutput import CornerDetectionOutput
from com.deepvision.tools.AngleDetectionTool import AngleDetectionTool
from com.deepvision.input.AngleDetectionInput import AngleDetectionInput
from com.deepvision.output.AngleDetectionOutput import AngleDetectionOutput
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.constants import Constant
from com.deepvision.job.JobLoader import JobLoader


def main():
    toolEngine = ToolEngine();
    jobLoader = JobLoader();
    jobLoader.loadJob();
    print(len(jobLoader.tool_list))

    for tool in jobLoader.tool_list:
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

        output = toolEngine.applyTool(tool)

        for next_tool in tool.next_tool:
            if (ToolType.CORNER_DETECTION.value == next_tool['type']):
                toolEngine.registerTool(CornerDetectionTool())
                next_tool_input = jobLoader.createCornerDetectionInput(next_tool);

            if (ToolType.TEMPLATE_MATCHING.value == next_tool.type):
                toolEngine.registerTool(TemplateMatchingTool())
                next_tool_input = jobLoader.createTemplateMatchingInput(next_tool);

            if (ToolType.ANGLE_DETECTION.value == next_tool.type):
                toolEngine.registerTool(AngleDetectionTool())
                next_tool_input = jobLoader.createAngleDetectionInput(next_tool);
                next_tool.point_1 = output.point_1
                next_tool.point_2 = output.point_2

            if (ToolType.DISTANCE_DETECTION.value == next_tool.type):
                toolEngine.registerTool(DistanceDetectionTool())
                next_tool_input = jobLoader.createDistanceDetectionInput(next_tool);
                next_tool.point_1 = output.point_1
                next_tool.point_2 = output.point_2

            if (ToolType.EDGE_DETECTION.value == next_tool.type):
                toolEngine.registerTool(EdgeDetectionTool())
                next_tool_input = jobLoader.createEdgeDetectionInput(next_tool);


if __name__ == "__main__":
    main();
