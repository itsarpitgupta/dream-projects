from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.constants import ToolType, Constant
from typing import TypeVar, Callable
from com.deepvision.output.CornerDetectionOutput import CornerDetectionOutput
from com.deepvision.input.CornerDetectionInput import CornerDetectionInput
import cv2
import numpy as np
import matplotlib.pyplot as plt


class CornerDetectionTool(ToolI):
    source_window = 'Source image'
    corners_window = 'Corners detected'
    max_thresh = 255

    def matches(type: ToolType) -> bool:
        return type == ToolType.ToolType.CORNER_DETECTION

    def process(self, input: CornerDetectionInput) -> CornerDetectionOutput:
        output = CornerDetectionOutput();
        if input.option == Constant.HARRIS_CORNER_DETECTION:
            output = self.harisCornerDetection(input.main_img, input.threshold, input.blockSize, input.apertureSize,
                                               input.k_size)
        else:
            output = ''
        return output;

    def harisCornerDetection(self, main_img, threshold, blockSize, apertureSize, k_size) -> CornerDetectionOutput:
        output = CornerDetectionOutput();
        full_img = cv2.imread(main_img)
        full = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)
        print(full.dtype)
        # Detecting corners
        dst = cv2.cornerHarris(full, 2, 3, 0.04)
        # Normalizing
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)

        # Drawing a circle around corners
        for i in range(dst_norm.shape[0]):
            for j in range(dst_norm.shape[1]):
                if int(dst_norm[i, j]) > threshold:
                    cv2.circle(dst_norm_scaled, (j, i), 5, (0), 2)
        # Showing the result

        output.status = Constant.RESULT_MATCH_FOUND

        plt.subplot(121), plt.imshow(full_img, cmap='gray')
        plt.title(self.source_window)  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(dst_norm_scaled, cmap='gray')
        plt.title(self.corners_window)  # , plt.xticks([]), plt.yticks([])
        plt.suptitle("Corner Detection" + " [" + output.status + "]")

        plt.show()

        return output
