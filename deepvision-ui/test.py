import os
import pickle
import socket
import sys

import cv2
import matplotlib.pyplot as plt
from PySide2 import QtGui, QtCore
from PySide2.QtGui import Qt, QPixmap, QPen, QColor, QBrush
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsEllipseItem, QTableWidgetItem

from deepvision.job.Job import Job
from deepvision.tools.CropTool import CropTool
from draggable_resizable_rectangle import GraphicsRectItem
from gui.ui_mainwindow import Ui_MainWindow
from model import Tool
from model.Output import Output
from model.TemplateMatching import TemplateMatching
from setup_image import SetupImageDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_29.clicked.connect(lambda: self.load_image())
        self.ui.pushButton_31.clicked.connect(lambda: self.add_tool_in_job())
        self.ui.pushButton_7.clicked.connect(lambda: self.edit_pattern_tool())
        self.ui.pushButton_8.clicked.connect(lambda: self.play())

        self.ui.treeWidget_2.doubleClicked.connect(self.show_tool_on_canvas)
        self.ui.stackedWidget.hide();
        self.add_tool_in_job()

    def edit_pattern_tool(self):
        self.ui.pushButton_7.setText("Train")
        scene = self.ui.graphicsView.scene()
        scene.addItem(self.search_item)
        scene.addItem(self.model_item)
        scene.removeItem(self.center_point)
        scene.update()

    @QtCore.Slot("QModelIndex")
    def show_tool_on_canvas(self, ix):
        if (ix.data() == 'Patterns'):
            self.ui.stackedWidget.show()
            scene = self.ui.graphicsView.scene()
            if scene is None:
                scene = QGraphicsScene()
            w = self.ui.graphicsView.size().width()
            h = self.ui.graphicsView.size().height()
            self.scene.setSceneRect(0, 0, w, h)
            self.ui.graphicsView.setScene(scene)
            self.search_item = GraphicsRectItem(0, 0, 200, 200, color=Qt.green, status_bar=self.ui.statusbar,
                                                showMarkers=True)
            scene.addItem(self.search_item)
            self.model_item = GraphicsRectItem(0, 0, 100, 100, color=Qt.red, status_bar=self.ui.statusbar,
                                               showMarkers=True)
            scene.addItem(self.model_item)

    def load_image(self):
        self.setupimage = SetupImageDialog()
        self.setupimage.setWindowModality(Qt.ApplicationModal)
        self.setupimage.dialog.buttonBox.accepted.connect(
            lambda: self.load_image_on_canvas("D://Vision_Application//hul_bad_230219\Bad//Image00114.BMP"))
        self.setupimage.exec_()

    def add_tool_in_job(self):
        getSelected = self.ui.treeWidget_2.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            if (getChildNode == 'Patterns'):
                self.ui.pushButton_7.setText("Model")
                print("Patterns Tool added")
                img = cv2.imread("D://Vision_Application//hul_bad_230219\Bad//Image00114.BMP", True)
                plt.imshow(img, cmap="hot")
                x = self.model_item.x() * 2
                y = self.model_item.y() * 2

                w = self.model_item.boundingRect().width() * 2 - 16
                h = self.model_item.boundingRect().height() * 2 - 16

                ct = CropTool()
                image = "D://Vision_Application//hul_bad_230219\Bad//Image00114.BMP"
                top_left = [int(x), int(y)]
                bottom_right = [int(w) + int(x), int(y) + int(h)]
                plt.scatter(int(w) + int(x), int(y) + int(h), s=50)

                output = ct.cropByPoints(image, top_left, bottom_right)
                template_path = "D:\github-repos\dream-projects\deepvision-py\DATA"
                cv2.imwrite(os.path.join(template_path, 'waka.jpg'), output.crop_image)
                pixmap = QPixmap("D:\github-repos\dream-projects\deepvision-py\DATA\waka.jpg")
                self.ui.label_11.setPixmap(pixmap)
                self.ui.label_11.show()

                scene = self.ui.graphicsView.scene()
                self.ui.graphicsView.setScene(scene)

                color = QPen(QColor(255, 0, 0))
                brush = QBrush(QColor(0, 255, 0))

                mid_x = int((top_left[0] + bottom_right[0]) / 4)
                mid_y = int((top_left[1] + bottom_right[1]) / 4)

                self.center_point = QGraphicsEllipseItem(mid_x, mid_y, 10, 10);
                self.center_point.setPen(color)
                self.center_point.setBrush(brush)
                scene.addItem(self.center_point)
                scene.removeItem(self.model_item)
                scene.removeItem(self.search_item)

                row_data = ["P", "Not Link", "Pattern", "Pattern Tool", "Pass", "Locate"]
                self.add_tool_in_result_table(row_data)
                top_left_pnt = []
                bottom_right_pnt = []
                tool_output = Output(top_left_pnt, bottom_right_pnt)
                template_matching_tool = TemplateMatching("",
                                                          "D:\github-repos\dream-projects\deepvision-py\DATA\waka.jpg",
                                                          "cv2.TM_CCOEFF_NORMED", "SINGLE", "TEMPLATE_MATCHING", "OFF",
                                                          tool_output, [])
                self.create_new_job(template_matching_tool)

    def load_image_on_canvas(self, image_path):
        self.scene = self.ui.graphicsView.scene()
        if self.scene is None:
            self.scene = QGraphicsScene(self)
        self.scene.clear()
        w = self.ui.graphicsView.size().width()
        h = self.ui.graphicsView.size().height()
        self.scene.setSceneRect(0, 0, w, h)
        pic = QtGui.QPixmap(image_path)
        pic2 = pic.scaled(w, h, Qt.IgnoreAspectRatio, Qt.FastTransformation)
        self.scene.addPixmap(pic2)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.update()
        return self.scene;

    def add_tool_in_result_table(self, row_data, rowPosition=0):
        rowPosition = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(rowPosition)
        i = 0
        for data in row_data:
            self.ui.tableWidget.setItem(rowPosition, i, QTableWidgetItem(data))
            i += 1

    def create_new_job(self, tool: Tool):
        self.tools = []
        self.tools.append(tool)
        self.job = Job("test_job", "test", "arpit", "na", "na", "na", self.tools, "OFF")
        # print(json.dumps(self.job))
        print(self.job.toJSON())

    def play(self):
        color = QPen(QColor(255, 0, 0))
        brush = QBrush(QColor(0, 255, 0))

        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 60000  # Reserve a port for your service.

        s.connect((host, port))
        while True:
            print('receiving data...')
            data = s.recv(1024)
            data_variable = pickle.loads(data)
            print(data_variable[0].img_path)
            self.scene = self.load_image_on_canvas(data_variable[0].img_path)
            if data_variable[0].result != "FAIL":
                x1 = int(data_variable[0].output.top_left_pnt[0] / 2)
                y1 = int(data_variable[0].output.top_left_pnt[1] / 2)
                x2 = int(data_variable[0].output.bottom_right_pnt[0] / 2)
                y2 = int(data_variable[0].output.bottom_right_pnt[1] / 2)
                w = int(x2 - x1)
                h = int(y2 - y1)
                self.model_item = GraphicsRectItem(x1, y1, w, h, color=QColor(255, 20, 147),
                                                   status_bar=self.ui.statusbar, showMarkers=False)

                mid_x = int((x1 * 2 + x2 * 2) / 4)
                mid_y = int((y1 * 2 + y2 * 2) / 4)
                self.center_point = QGraphicsEllipseItem(mid_x, mid_y, 10, 10);
                self.center_point.setPen(color)
                self.center_point.setBrush(brush)
                self.scene.addItem(self.center_point)
                self.scene.addItem(self.model_item)

            QApplication.processEvents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
