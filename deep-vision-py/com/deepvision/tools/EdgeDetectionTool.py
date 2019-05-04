from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.constants import ToolType, Constant
from typing import TypeVar, Callable
from com.deepvision.output.EdgeDetectionOutput import EdgeDetectionOutput
from com.deepvision.input.EdgeDetectionInput import EdgeDetectionInput
import cv2
import numpy as np
import matplotlib.pyplot as plt


class EdgeDetectionTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.EDGE_DETECTION

    def process(self, input: EdgeDetectionInput) -> EdgeDetectionOutput:
        output = EdgeDetectionOutput();
        if input.option == Constant.CANNY_EDGE_DETECTION:
            output = self.cannyEdgeDetection(input.main_img, input.lower_threshold, input.upper_threshold,
                                             input.k_sizeX, input.k_sizeY, input.edge_thickness)
        else:
            output = ToolType.NO_TOOL
        return output;

    def cannyEdgeDetection(self, main_img, lower, upper, ksizX, ksizeY, edge_thickness) -> EdgeDetectionOutput:
        output = EdgeDetectionOutput()
        full_img = cv2.imread(main_img)
        full_gray = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)

        # LOWER THRESHOLD TO EITHER 0 OR 70% OF THE MEDIAN VALUE WHICH EVER IS GREATER
        lower = int(max(0, 0.7 * np.median(full_gray)))
        # UPPER THRESHOLD TO EITHER 130% OF THE MEDIAN VALUE OF THE 255, WHICH EVER IS SMALLER
        upper = int(min(255, 1.3 * np.median(full_gray)))

        blurred_img = cv2.blur(full_gray, ksize=(ksizX, ksizeY))

        edges = cv2.Canny(blurred_img, threshold1=lower, threshold2=upper)

        rows = edges[:, 1].size
        cols = edges[1, :].size

        count = 1
        for x in range(0, rows):
            for y in range(0, cols):
                if edges[x, y] == 255:
                    for t in range(y + 1, y + edge_thickness):
                        if t < cols:
                            if edges[x, t] == 255:
                                count += 1
                            else:
                                break
                    if count >= edge_thickness:
                        output.points.append([x, y])
                count = 1
        # Showing the result

        plt.subplot(121), plt.imshow(full_img, cmap='gray')
        plt.title('Original Image')  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Detection')  # , plt.xticks([]), plt.yticks([])
        plt.show()

        output.status = Constant.RESULT_MATCH_FOUND
        return output;