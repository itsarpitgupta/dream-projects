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


class ToolProcessor:

    def __init__(self, result_dict):
        self.result_dict = result_dict

