from ToolI import ToolI
from ToolType import ToolType
from typing import TypeVar, Callable
from TemplateMatchingOutput import TemplateMatchingOutput
from TemplateMatchingInput import TemplateMatchingInput


class TemplateMatchingTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.TEMPLATE_MATCHING

    def process(self, input: TemplateMatchingInput) -> TemplateMatchingOutput:
        output = TemplateMatchingOutput();
        output.status = 'FAIL';
        return output;
