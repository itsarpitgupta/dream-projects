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
        if input.method == Constant.HARRIS_CORNER_DETECTION:
            output = self.harisCornerDetection(input.main_img, input.threshold, input.blockSize, input.apertureSize,
                                               input.k_size)
        elif input.method == Constant.SHI_TOMASI_AND_GOOD_FEATURES_TO_TRACK_CORNER_DETECTION:
            output = self.shiTomasiAndGoodFeaturesToTrack(input.main_img, input.maxCorners)
        else:
            output = ''
        return output;

    def harisCornerDetection(self, main_img, threshold, blockSize, apertureSize, k_size) -> CornerDetectionOutput:
        output = CornerDetectionOutput();
        full_img = cv2.imread(main_img)
        full = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)
        # Detecting corners
        dst = cv2.cornerHarris(full, blockSize, apertureSize, k_size)
        # Normalizing
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)

        # Drawing a circle around corners
        for i in range(dst_norm.shape[0]):
            for j in range(dst_norm.shape[1]):
                if int(dst_norm[i, j]) > threshold:
                    print("(", i, ",", j, ")")
                    output.corners.append([x, y])
                    cv2.circle(dst_norm_scaled, (j, i), 5, (0), 5)
        # Showing the result

        output.status = Constant.RESULT_MATCH_FOUND
        output.point_1 = output.corners[0]
        output.point_2 = output.corners[-1]

        plt.subplot(121), plt.imshow(full_img, cmap='gray')
        plt.title(self.source_window)  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(dst_norm_scaled, cmap='gray')
        plt.title(self.corners_window)  # , plt.xticks([]), plt.yticks([])
        plt.suptitle("Corner Detection" + " [" + output.status + "]")

        plt.show()

        return output

    def shiTomasiAndGoodFeaturesToTrack(self, main_img, maxCorners) -> CornerDetectionOutput:
        output = CornerDetectionOutput();
        full_img = cv2.imread(main_img)
        full = cv2.cvtColor(full_img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(full, maxCorners, 0.01, 10)
        corners = np.int0(corners)

        # Drawing a circle around corners
        for i in corners:
            x, y = i.ravel()
            output.corners.append([x, y])
            cv2.circle(full, (x, y), 3, (0, 255, 0), 5)

        # Showing the result
        output.status = Constant.RESULT_MATCH_FOUND
        output.point_1 = output.corners[0]
        output.point_2 = output.corners[-1]


        plt.subplot(121), plt.imshow(full_img, cmap='gray')
        plt.title(self.source_window)  # , plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(full, cmap='gray')
        plt.title(self.corners_window)  # , plt.xticks([]), plt.yticks([])
        plt.suptitle("Corner Detection" + " [" + output.status + "]")

        plt.show()

        return output
