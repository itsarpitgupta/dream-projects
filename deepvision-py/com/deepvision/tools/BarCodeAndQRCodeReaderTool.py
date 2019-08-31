import cv2
from pyzbar import pyzbar

from com.deepvision.constants import Constant
from com.deepvision.constants.ToolType import ToolType
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.BarCodeAndQRCodeInput import BarCodeAndQRCodeInput
from com.deepvision.output.BarCodeAndQRCodeReaderOutput import BarCodeAndQRCodeReaderOutput
from com.deepvision.output.FixtureOutput import FixtureOutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import displayImageOutput


class BarCodeAndQRCodeReaderTool(ToolI):

    def matches(type: ToolType) -> bool:
        return type == ToolType.BAR_CODE_AND_QR_CODE

    def process(self, input: BarCodeAndQRCodeInput) -> BarCodeAndQRCodeReaderOutput:
        return self.readCode(input.main_img)

    def readCode(self, main_img) -> FixtureOutput:
        output = BarCodeAndQRCodeReaderOutput()
        try:
            if main_img is None:
                raise DataValidationException('main image should not be none')

            # reading the main image
            if isinstance(main_img, str):
                img_gray = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)
            else:
                img_gray = main_img

            # find the barcodes in the image and decode each of the barcodes
            barcodes = pyzbar.decode(img_gray)

            # loop over the detected barcodes
            for barcode in barcodes:
                # extract the bounding box location of the barcode and draw the
                # bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(img_gray, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # the barcode data is a bytes object so if we want to draw it on
                # our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                output.text.append(text)

            if self.display:
                displayImageOutput(main_img=main_img, main_img_title="Main Image", result_img=img_gray,
                                   result_img_title="Code Reader", title="Bar Code and QR code Reader")



        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output
