import ToolI
from ToolType import ToolType
from typing import TypeVar
import TemplateMatchingOutput
import TemplateMatchingInput

TemplateMatchingInput = TypeVar('TemplateMatchingInput')      # Declare input type variable
TemplateMatchingOutput = TypeVar('TemplateMatchingOutput')      # Declare output type variable


class TemplateMatchingTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.TEMPLATE_MATCHING

    def proces(self,input:TemplateMatchingInput)-> TemplateMatchingOutput:
        output = TemplateMatchingOutput();
        output.status = 'FAIL';
        return output;
