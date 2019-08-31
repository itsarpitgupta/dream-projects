from abc import ABC
from typing import TypeVar, Generic

from com.deepvision.constants import ToolType

I = TypeVar('I')  # Declare input type variable
O = TypeVar('O')  # Declare output type variable


class ToolI(ABC, Generic[I, O]):
    # abstract method
    def matches(type: ToolType) -> bool:
        pass

    def process(self, input: I) -> O:
        pass

    display = False
