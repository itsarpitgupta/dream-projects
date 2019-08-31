from com.deepvision.output.BaseOutput import BaseOutput


class CornerDetectionOutput(BaseOutput):
    status = 'PASS'
    corners = []
    point_1 = []
    point_2 = []

    def __init__(self):
        super(CornerDetectionOutput, self).__init__()