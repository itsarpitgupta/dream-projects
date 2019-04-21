from abc import ABC, abstractmethod
from ToolType import ToolType
from typing import TypeVar,Generic

I = TypeVar('I')      # Declare input type variable
O = TypeVar('O')      # Declare output type variable

class ToolI(ABC,Generic[I,O]):
    # abstract method
    def matches(type: ToolType) -> bool:
        pass

    def process(self,input:I)-> O:
        pass