import numpy as np
import cv2
from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.TextDetectionInput import TextDetectionInput
from com.deepvision.output.TextDetectionOutput import TextDetectionOutput
from com.deepvision.toolengine.ToolI import ToolI
from imutils.object_detection import non_max_suppression
from com.deepvision.util.displayutil import displayImageOutput


class TextDetectionTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.TEXT_DETECTION

    def process(self, input: TextDetectionInput) -> TextDetectionOutput:
        return self.find_text_area(main_img=input.main_img, threshold=input.threshold, width=input.width,
                                   height=input.height)

    def find_text_area(self, main_img, threshold, width, height) -> TextDetectionOutput:
        output = TextDetectionOutput()
        try:
            if threshold is None or width is None or height is None or main_img is None:
                raise DataValidationException('threshold, main_img ,width, or height should not be none')

            # reading the main image
            if isinstance(main_img, str):
                img_gray = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)
            else:
                img_gray = main_img

            # load the input image and grab the image dimensions
            orig = img_gray.copy()
            (H, W) = img_gray.shape[:2]

            # set the new width and height and then determine the ratio in change
            # for both the width and height
            (newW, newH) = (width, height)
            rW = W / float(newW)
            rH = H / float(newH)

            # resize the image and grab the new image dimensions
            img_gray = cv2.resize(img_gray, (newW, newH))
            (H, W) = img_gray.shape[:2]

            # define the two output layer names for the EAST detector model that
            # we are interested -- the first is the output probabilities and the
            # second can be used to derive the bounding box coordinates of text
            layerNames = [
                "feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"]

            # load the pre-trained EAST text detector
            print("[INFO] loading EAST text detector...")
            net = cv2.dnn.readNet(
                '..//..//..//training-models//frozen_east_text_detection.pb')

            # construct a blob from the image and then perform a forward pass of
            # the model to obtain the two output layer sets
            blob = cv2.dnn.blobFromImage(img_gray, 1.0, (W, H),
                                         (123.68, 116.78, 103.94), swapRB=True, crop=False)
            net.setInput(blob)
            (scores, geometry) = net.forward(layerNames)

            # grab the number of rows and columns from the scores volume, then
            # initialize our set of bounding box rectangles and corresponding
            # confidence scores
            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []

            # loop over the number of rows
            for y in range(0, numRows):
                # extract the scores (probabilities), followed by the geometrical
                # data used to derive potential bounding box coordinates that
                # surround text
                scoresData = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]

                # loop over the number of columns
                for x in range(0, numCols):
                    # if our score does not have sufficient probability, ignore it
                    if scoresData[x] < threshold:
                        continue

                    # compute the offset factor as our resulting feature maps will
                    # be 4x smaller than the input image
                    (offsetX, offsetY) = (x * 4.0, y * 4.0)

                    # extract the rotation angle for the prediction and then
                    # compute the sin and cosine
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    # use the geometry volume to derive the width and height of
                    # the bounding box
                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]

                    # compute both the starting and ending (x, y)-coordinates for
                    # the text prediction bounding box
                    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                    startX = int(endX - w)
                    startY = int(endY - h)

                    # add the bounding box coordinates and probability score to
                    # our respective lists
                    rects.append((startX, startY, endX, endY))
                    confidences.append(scoresData[x])

            # apply non-maxima suppression to suppress weak, overlapping bounding
            # boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)
            point_result = []
            # loop over the bounding boxes
            for (startX, startY, endX, endY) in boxes:
                # scale the bounding box coordinates based on the respective
                point_result.append([startX, startY, endX, endY])

                # ratios
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)

                # show the output image
                if self.display:
                    # draw the bounding box on the image
                    cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    displayImageOutput(main_img=img_gray, main_img_title="Main Image", result_img=orig,
                                       result_img_title="Detected Text", title="Text Detection")


            output.status = Constant.TOOL_PASS
            output.box_lists = point_result
        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
