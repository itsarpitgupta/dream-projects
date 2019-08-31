import cv2 as cv2
import numpy as np
from scipy._lib.six import xrange
from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.CropInput import CropInput
from com.deepvision.output.CropOutput import CropOutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import displayImageOutput


class CropTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.CROP

    def process(self, input: CropInput) -> CropOutput:
        if input.method == Constant.CROP_BY_POINT:
            output = self.cropByPoints(input.main_img, input.top_left, input.bottom_right)
        elif input.method == Constant.CROP_BY_PERCENTAGE:
            output = self.cropByPercentage(input.main_img, input.start_percentage, input.end_percentage)
        return output

    def cropByPoints(self, main_img, top_left, bottom_right) -> CropOutput:
        output = CropOutput()
        try:
            # validate the points
            if main_img is None or top_left is None or bottom_right is None:
                raise DataValidationException("main_img, top_left or bottom_right should not be None")

            if isinstance(main_img, str):
                img = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)
            else:
                img = main_img

            x1, y1 = top_left[0], top_left[1]
            x2, y2 = bottom_right[0], bottom_right[1]
            cropped = img[y1:y2, x1:x2]

            if self.display:
                displayImageOutput(main_img=img, main_img_title="Main Img", result_img=cropped,
                                   result_img_title="Cropped Point", title="Crop By Points")

            output.crop_image = cropped
            output.status = Constant.TOOL_PASS

        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output

    def cropByPercentage(self, main_img, start_percentage, end_percentage) -> CropOutput:
        output = CropOutput()
        img = cv2.imread(main_img)

        h, w = img.shape[:2]

        x1, y1 = int(h * start_percentage), int(w * start_percentage)

        x2, y2 = int(h * end_percentage), int(w * end_percentage)

        cropped = img[x1:x2, y1:y2]

        if self.display:
            displayImageOutput(main_img=img, main_img_title="Main Img", result_img=cropped,
                               result_img_title="Cropped Point", title="Crop By Percentage")

        output.crop_image = cropped
        output.status = Constant.TOOL_PASS

        return output

    """
    This method can crop only triangle with low level performance
    """

    def cropTriangle(self, main_img, point_1, point_2, point_3):
        # Read input image
        imgIn = cv2.imread(main_img)

        # Output image is set to white
        imgOut = 255 * np.ones(imgIn.shape, dtype=imgIn.dtype)

        # Input triangle
        triIn = np.float32([[point_1, point_2, point_3]])

        # Output triangle
        triOut = np.float32([[point_1, point_2, point_3]])

        # Warp all pixels inside input triangle to output triangle
        warpTriangle(imgIn, imgOut, triIn, triOut)

        # Draw triangle using this color
        color = (255, 150, 0)

        # Draw triangles in input and output images.
        # cv2.polylines(imgIn, triIn.astype(int), True, color, 2, 16)
        # cv2.polylines(imgOut, triOut.astype(int), True, color, 2, 16)

        if self.display:
            displayImageOutput(main_img=imgIn, main_img_title="main_image", result_img=imgOut,
                               result_img_title="result_image", title="Triangle Cropping")

    """
    Points List should contain point in bottom left, bottom right , top right , top left format only.  
    By using this method we can crop triangle, rectangle, non rectangle and polygon etc..   
    """

    def cropPolygon(self, main_img, pointsList):

        img = cv2.imread(main_img)
        pts = np.array([pointsList])

        # testing
        # pts = np.array([[10, 150], [150, 100], [300, 150], [350, 100], [310, 20], [35, 10]])
        # pts = np.array([[100, 300], [400, 300], [400, 100], [100, 100]])
        # pts = np.array([[100, 300], [400, 300], [250, 100]])
        # xpoint = [100, 400, 250]
        # ypoint = [300, 300, 100]
        # draw_multiple_points(xpoint, ypoint, "fghd")

        ## (1) Crop the bounding rect
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        croped = img[y:y + h, x:x + w].copy()

        ## (2) make mask
        pts = pts - pts.min(axis=0)

        mask = np.zeros(croped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ## (3) do bit-op
        dst = cv2.bitwise_and(croped, croped, mask=mask)

        ## (4) add the white background
        bg = np.ones_like(croped, np.uint8) * 255
        cv2.bitwise_not(bg, bg, mask=mask)
        dst2 = bg + dst

        if self.display:
            displayImageOutput(main_img=img, main_img_title="main_image", result_img=dst2,
                               result_img_title="result_image", title="Polygon Cropping")


def warpTriangle(img1, img2, tri1, tri2):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(tri1)
    r2 = cv2.boundingRect(tri2)

    # Offset points by left top corner of the respective rectangles
    tri1Cropped = []
    tri2Cropped = []

    for i in xrange(0, 3):
        tri1Cropped.append(((tri1[0][i][0] - r1[0]), (tri1[0][i][1] - r1[1])))
        tri2Cropped.append(((tri2[0][i][0] - r2[0]), (tri2[0][i][1] - r2[1])))

    # Crop input image
    img1Cropped = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(tri1Cropped), np.float32(tri2Cropped))

    # Apply the Affine Transform just found to the src image
    img2Cropped = cv2.warpAffine(img1Cropped, warpMat, (r2[2], r2[3]), None, flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_REFLECT_101)

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(tri2Cropped), (1.0, 1.0, 1.0), 16, 0);

    img2Cropped = img2Cropped * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
            (1.0, 1.0, 1.0) - mask)

    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Cropped
