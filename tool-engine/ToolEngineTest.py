import ToolEngine
import TemplateMatchingTool
import TemplateMatchingInput
from ToolType import ToolType

class ToolEngineTest(object):

    def main(self):
        toolEngine = ToolEngine()
        toolEngine.registerTool(TemplateMatchingTool())

        baseInput = TemplateMatchingInput()
        baseInput.type = ToolType.TEMPLATE_MATCHING

        baseOutput = toolEngine.applyTool(baseInput)

        print(baseOutput)


    if __name__ == '__main__':
        main();