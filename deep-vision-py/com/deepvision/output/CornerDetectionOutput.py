from BaseOutput import BaseOutput


class CornerDetectionOutput(BaseOutput):
    status = 'PASS'
    corners = []

    def __init__(self):
        super(CornerDetectionOutput, self).__init__()
        print("corner detection init")