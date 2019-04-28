from com.deepvision.toolengine.ToolEngine import ToolEngine
from com.deepvision.tools.TemplateMatchingTool import TemplateMatchingTool
from com.deepvision.tools.CornerDetectionTool import CornerDetectionTool
from com.deepvision.input.TemplateMatchingInput import TemplateMatchingInput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.constants import Constant

class ToolEngineTest(object):

    def main(self):
        toolEngine = ToolEngine()
        # Tool :1
        toolEngine.registerTool(TemplateMatchingTool())
        baseInput = TemplateMatchingInput()
        baseInput.main_img = 'D:\github-repos\dream-projects\deep-vision-py\DATA\Image00111.BMP'
        baseInput.temp_img = 'D:\github-repos\dream-projects\deep-vision-py\DATA\\template.jpg'
        baseInput.option = Constant.TEMPLATE_MATCHING_ON_MULTIPLE_OBJECT
        baseInput.type = ToolType.TEMPLATE_MATCHING

        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput.status)

        #Tool :2
        toolEngine.registerTool(CornerDetectionTool())
        baseInput = CornerDetectionInput()
        baseInput.main_img = 'D:\github-repos\dream-projects\deep-vision-py\DATA\\flat_chessboard.png'
        baseInput.option = Constant.HARRIS_CORNER_DETECTION
        baseInput.type = ToolType.CORNER_DETECTION

        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput.status)

if __name__ == '__main__':
    test = ToolEngineTest().main()
