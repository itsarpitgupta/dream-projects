from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.input.AngleDetectionInput import AngleDetectionInput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.input.EdgeDetectionInput import EdgeDetectionInput
from com.deepvision.toolengine.ToolEngine import ToolEngine
from com.deepvision.tools.AngleDetectionTool import AngleDetectionTool
from com.deepvision.tools.CornerDetectionTool import CornerDetectionTool
from com.deepvision.tools.EdgeDetectionTool import EdgeDetectionTool


class ToolEngineTest(object):

    def main(self):
        toolEngine = ToolEngine()
        # Tool :1
        """
        toolEngine.registerTool(TemplateMatchingTool())
        baseInput = TemplateMatchingInput()
        baseInput.main_img = 'D:\github-repos\dream-projects\deep-vision-py\DATA\Image00111.BMP'
        baseInput.temp_img = 'D:\github-repos\dream-projects\deep-vision-py\DATA\\template.jpg'
        baseInput.option = Constant.TEMPLATE_MATCHING_ON_MULTIPLE_OBJECT
        baseInput.type = ToolType.TEMPLATE_MATCHING

        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput.status)
        """
    
        #Tool :2
        toolEngine.registerTool(CornerDetectionTool())
        baseInput = CornerDetectionInput()
        baseInput.main_img = 'C:/Users/arpit-java/Pictures/img.jpg'
        baseInput.option = Constant.SHI_TOMASI_AND_GOOD_FEATURES_TO_TRACK_CORNER_DETECTION
        baseInput.type = ToolType.CORNER_DETECTION
        # baseInput.threshold = 100
        baseInput.maxCorners = 4
        baseOutput = toolEngine.applyTool(baseInput)
        print(baseOutput.corners)
        


        #Tool :3
        toolEngine.registerTool(EdgeDetectionTool())
        baseInput = EdgeDetectionInput()
        baseInput.main_img = 'D:\Vision_Application\hul_bad_230219\Bad\Image00111.BMP'
        baseInput.option = Constant.CANNY_EDGE_DETECTION
        baseInput.type = ToolType.EDGE_DETECTION
        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput.points)

        #Tool :4
        toolEngine.registerTool(AngleDetectionTool())
        baseInput = AngleDetectionInput()
        baseInput.point_1 = baseOutput.points[0]
        baseInput.point_2 = baseOutput.points[-1]
        baseInput.type = ToolType.ANGLE_DETECTION
        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput.angle_value)

if __name__ == '__main__':
    test = ToolEngineTest().main()
