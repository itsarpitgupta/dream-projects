from abc import ABC, abstractmethod
import ToolType
from typing import TypeVar


I = TypeVar('I')      # Declare input type variable
O = TypeVar('O')      # Declare output type variable

class ToolI(ABC):
    # abstract method
    def matches(type: ToolType) -> bool:
        pass

    def proces(self,input:I)-> O:
        pass