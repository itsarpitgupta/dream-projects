import cv2 as cv2
import pytesseract
from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.TextRecoginationInput import TextRecoginationInput
from com.deepvision.output.TextRecoginationOutput import TextRecoginationOutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import displayImageOutput


class TextRecoginationTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.TEXT_RECOGINATION

    def process(self, input: TextRecoginationInput) -> TextRecoginationOutput:
        return self.recogination_text(main_img=input.main_img, box_lists=input.box_lists, paddings=input.padding,
                                      width=320, height=320)

    def recogination_text(self, main_img, box_lists, paddings, width, height) -> TextRecoginationOutput:
        output = TextRecoginationOutput()
        try:
            if box_lists is None or paddings is None or main_img is None:
                raise DataValidationException('box_lists, main_img or paddings should not be none')

            # reading the main image
            if isinstance(main_img, str):
                img_gray = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)
            else:
                img_gray = main_img

            # load the input image and grab the image dimensions
            orig = img_gray.copy()
            (origH, origW) = img_gray.shape[:2]

            (newW, newH) = (width, height)
            rW = origW / float(newW)
            rH = origH / float(newH)

            # initialize the list of results
            results = []
            text_result = []
            # loop over the bounding boxes
            for (startX, startY, endX, endY) in box_lists:
                # scale the bounding box coordinates based on the respective
                # ratios
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)

                # in order to obtain a better OCR of the text we can potentially
                # apply a bit of padding surrounding the bounding box -- here we
                # are computing the deltas in both the x and y directions
                dX = int((endX - startX) * paddings)
                dY = int((endY - startY) * paddings)

                # apply padding to each side of the bounding box, respectively
                startX = max(0, startX - dX)
                startY = max(0, startY - dY)
                endX = min(origW, endX + (dX * 2))
                endY = min(origH, endY + (dY * 2))

                # extract the actual padded ROI
                roi = orig[startY:endY, startX:endX]

                # in order to apply Tesseract v4 to OCR text we must supply
                # (1) a language, (2) an OEM flag of 4, indicating that the we
                # wish to use the LSTM neural net model for OCR, and finally
                # (3) an OEM value, in this case, 7 which implies that we are
                # treating the ROI as a single line of text
                config = ("-l eng --oem 1 --psm 7")
                text = pytesseract.image_to_string(roi, config=config)

                # add the bounding box coordinates and OCR'd text to the list
                # of results
                results.append(((startX, startY, endX, endY), text))

            # sort the results bounding box coordinates from top to bottom
            results = sorted(results, key=lambda r: r[0][1])

            # loop over the results
            for ((startX, startY, endX, endY), text) in results:
                # display the text OCR'd by Tesseract
                print("OCR TEXT")
                print("========")
                print("{}\n".format(text))


                # strip out non-ASCII text so we can draw the text on the image
                # using OpenCV, then draw the text and a bounding box surrounding
                # the text region of the input image
                text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

                if self.display:
                    # draw the bounding box on the image
                    output_cpy = orig.copy()
                    cv2.rectangle(output_cpy, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    cv2.putText(output_cpy, text, (startX, startY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                    displayImageOutput(main_img=img_gray, main_img_title="Main Image", result_img=output_cpy,
                                       result_img_title="Detected Text", title="Text Recogination")

                text_result.append(text)

            output.text_lists = text_result
            output.status = Constant.TOOL_PASS
        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
