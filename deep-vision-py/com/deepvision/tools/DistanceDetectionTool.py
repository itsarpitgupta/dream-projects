from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.constants import ToolType, Constant
from com.deepvision.input.DistanceDetectionInput import DistanceDetectionInput
from com.deepvision.output.DistanceDetectionOutput import DistanceDetectionOutput
from typing import TypeVar, Callable
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance as dist


class DistanceDetectionTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.DISTANCE_DETECTION

    def process(self, input: DistanceDetectionInput) -> DistanceDetectionOutput:
        if input.option == Constant.CANNY_EDGE_DETECTION:
            output = self.distanceDetection(input.method,input.point_1,input.point_2)
        else:
            output = ToolType.NO_TOOL
        return output;

    def distanceDetection(self, method, point_1, point_2) -> DistanceDetectionOutput:
        output = DistanceDetectionOutput()
        output.total_distance = dist.euclidean(point_1, point_2)
        output.status = Constant.RESULT_MATCH_FOUND
        return output;