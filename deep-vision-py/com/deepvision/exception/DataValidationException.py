from com.deepvision.exception.BusinessException import BusinessException


class DataValidationException(BusinessException):

    # Constructor or Initializer
    def __init__(self, msg):
        self.msg = msg

    # __str__ is to print() the value
    def __str__(self):
        return (repr(self.msg))
