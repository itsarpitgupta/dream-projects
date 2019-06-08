import threading
import time
from com.deepvision.constants import Constant
from com.deepvision.models.ImageData import ImageData
import cv2 as cv2


class ImageLoaderThread(threading.Thread):

    def __init__(self, name, imageProcessQueue):
        threading.Thread.__init__(self)
        self.name = name
        self.imageProcessQueue = imageProcessQueue

    def run(self):
        self.loadImages()

    def loadImages(self):
        for i in range(12):
            # img = ImageData()
            # img.image_name = 'Image001{}.{}'.format(i, ".BMP")
            # img.image_path = Constant.IMAGE_PATH
            # img.image = cv2.imread(img.image_path + "\\" + img.image_name, 0)

            # self.imageProcessQueue.put(Constant.IMAGE_PATH+"\\"+'Image001{}{}'.format(i+14, ".BMP"))
            # self.imageProcessQueue.put("D:\Vision_Application\OCR\OCR 9\\" + 'example_0{}{}'.format(i+1, ".jpg"))
            self.imageProcessQueue.put("D:\\Vision_Application\\ffc\\" + 'Image000{}{}'.format(i+12, ".BMP"))
            # print('loading images... {}'.format(Constant.IMAGE_PATH+"\\"+'Image001{}{}'.format(i+14, ".BMP")))
            time.sleep(.1)
