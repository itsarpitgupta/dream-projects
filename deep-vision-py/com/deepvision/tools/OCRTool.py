import cv2
import numpy as np

from com.deepvision.constants import ToolType, Constant
from com.deepvision.exception.DataValidationException import DataValidationException
from com.deepvision.input.OCRInput import OCRInput
from com.deepvision.output import OCROutput
from com.deepvision.toolengine.ToolI import ToolI
from com.deepvision.util.displayutil import displayImageOutput

# module level variables ##########################################################################
# MIN_CONTOUR_AREA = 30
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30
###################################################################################################

class OCRTool(ToolI):


    # member variables ############################################################################

    npaContour = None  # contour
    boundingRect = None  # bounding rect for contour
    intRectX = 0  # bounding rect top left corner x location
    intRectY = 0  # bounding rect top left corner y location
    intRectWidth = 0  # bounding rect width
    intRectHeight = 0  # bounding rect height
    fltArea = 0.0  # area of contour


    def matches(type: ToolType) -> bool:
        return type == ToolType.OCR

    def process(self, input: OCRInput) -> OCROutput:
        return self.ocr_detection_using_knn(input.main_img, input.min_counter_area)

    def ocr_detection_using_knn(self, main_img, max_counter_area) -> OCROutput:
        output = OCROutput()
        try:
            # validate the points
            if main_img is None or max_counter_area is None:
                raise DataValidationException("main_img and max_counter_area should not be None")

            # reading the main image
            if isinstance(main_img, str):
                imgTestingNumbers = cv2.imread(main_img, cv2.IMREAD_GRAYSCALE)
            else:
                imgTestingNumbers = main_img

            allContoursWithData = []  # declare empty lists,
            validContoursWithData = []  # we will fill these shortly

            try:
                npaClassifications = np.loadtxt("..//..//..//training-models//classifications.txt", np.float32)  # read in training classifications
            except:
                print("error, unable to open classifications.txt, exiting program\n")
                return
            # end try

            try:
                npaFlattenedImages = np.loadtxt("..//..//..//training-models//flattened_images.txt", np.float32)  # read in training images
            except:
                print("error, unable to open flattened_images.txt, exiting program\n")
                return
            # end try

            npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))  # reshape numpy array to 1d, necessary to pass to call to train

            kNearest = cv2.ml.KNearest_create()  # instantiate KNN object

            kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)



            if imgTestingNumbers is None:  # if image was not read successfully
                print("error: image not read from file \n\n")  # print error message to std out
                return  # and exit function (which exits program)
            # end if

            imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)  # get grayscale image
            imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)  # blur

            # filter image from grayscale to black and white
            imgThresh = cv2.adaptiveThreshold(imgBlurred,  # input image
                                              255,  # make pixels that pass the threshold full white
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              # use gaussian rather than mean, seems to give better results
                                              cv2.THRESH_BINARY_INV,
                                              # invert so foreground will be white, background will be black
                                              11,  # size of a pixel neighborhood used to calculate threshold value
                                              2)  # constant subtracted from the mean or weighted mean

            imgThreshCopy = imgThresh.copy()  # make a copy of the thresh image, this in necessary b/c findContours modifies the image

            npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,
                                                         # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                         cv2.RETR_EXTERNAL,  # retrieve the outermost contours only
                                                         cv2.CHAIN_APPROX_SIMPLE)  # compress horizontal, vertical, and diagonal segments and leave only their end points

            for npaContour in npaContours:  # for each contour
                contourWithData = self.ContourWithData()  # instantiate a contour with data object
                contourWithData.npaContour = npaContour  # assign contour to contour with data
                contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)  # get the bounding rect
                contourWithData.calculateRectTopLeftPointAndWidthAndHeight()  # get bounding rect info
                contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)  # calculate the contour area
                allContoursWithData.append(
                    contourWithData)  # add contour with data object to list of all contours with data
            # end for

            for contourWithData in allContoursWithData:  # for all contours
                if contourWithData.checkIfContourIsValid(min_counter_area=max_counter_area):  # check if valid
                    validContoursWithData.append(contourWithData)  # if so, append to valid contour list
                # end if
            # end for

            validContoursWithData.sort(key=self.operator.attrgetter("intRectX"))  # sort contours from left to right

            strFinalString = ""  # declare final string, this will have the final number sequence by the end of the program

            for contourWithData in validContoursWithData:  # for each contour
                # draw a green rect around the current char
                cv2.rectangle(imgTestingNumbers,  # draw rectangle on original testing image
                              (contourWithData.intRectX, contourWithData.intRectY),  # upper left corner
                              (contourWithData.intRectX + contourWithData.intRectWidth,
                               contourWithData.intRectY + contourWithData.intRectHeight),  # lower right corner
                              (0, 255, 0),  # green
                              1)  # thickness

                imgROI = imgThresh[contourWithData.intRectY: contourWithData.intRectY + contourWithData.intRectHeight,
                         # crop char out of threshold image
                         contourWithData.intRectX: contourWithData.intRectX + contourWithData.intRectWidth]

                imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH,RESIZED_IMAGE_HEIGHT))  # resize image, this will be more consistent for recognition and storage

                npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image into 1d numpy array

                npaROIResized = np.float32(npaROIResized)  # convert from 1d numpy array of ints to 1d numpy array of floats

                retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k=1)  # call KNN function find_nearest

                # print('{} - {}'.format(dists[0][0],str(chr(int(npaResults[0][0])))))
                if dists[0][0] != 0.0:
                    strCurrentChar = '?'
                else:
                    strCurrentChar = str(chr(int(npaResults[0][0])))  # get character from results

                strFinalString = strFinalString + strCurrentChar  # append current char to full string
            # end for

            cv2.putText(imgTestingNumbers, strCurrentChar, (contourWithData.intRectX, contourWithData.intRectY),
                        cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)

            if self.display:
                displayImageOutput(main_img=imgTestingNumbers, main_img_title="Matching Result", result_img=imgTestingNumbers,
                                   result_img_title="Character Detection", title="OCR")


            output.text_result = strFinalString
            output.status = Constant.TOOL_PASS
        except DataValidationException as data_exp:
            print('DataValidationException :', data_exp.msg)
            output.status = Constant.TOOL_FAIL
        except Exception as exp:
            print('Exception : ', exp.args)
            output.status = Constant.TOOL_FAIL

        return output



    def calculateRectTopLeftPointAndWidthAndHeight(self):  # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self, min_counter_area):  # this is oversimplified, for a production grade program
        if self.fltArea < min_counter_area: return False  # much better validity checking would be necessary
        return True