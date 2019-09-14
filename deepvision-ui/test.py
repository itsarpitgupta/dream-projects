import os
import sys

import cv2
import matplotlib.pyplot as plt
from PySide2 import QtGui, QtCore
from PySide2.QtGui import Qt, QPixmap, QPen, QColor, QBrush
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsEllipseItem

from deepvision.tools.CropTool import CropTool
from draggable_resizable_rectangle import GraphicsRectItem
from gui.ui_mainwindow import Ui_MainWindow
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

        self.ui.treeWidget_2.doubleClicked.connect(self.show_tool_on_canvas)
        self.ui.stackedWidget.hide();
        self.add_tool_in_job()

    def edit_pattern_tool(self):
        self.ui.pushButton_7.setText("Train")
        scene = self.ui.graphicsView.scene()
        scene.addItem(self.search_item)
        scene.addItem(self.model_item)
        scene.removeItem(self.center_point)

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
            self.search_item = GraphicsRectItem(0, 0, 200, 200, color=Qt.green, status_bar=self.ui.statusbar)
            scene.addItem(self.search_item)
            self.model_item = GraphicsRectItem(0, 0, 100, 100, color=Qt.red, status_bar=self.ui.statusbar)
            scene.addItem(self.model_item)

    def load_image(self):
        self.setupimage = SetupImageDialog()
        self.setupimage.setWindowModality(Qt.ApplicationModal)
        self.setupimage.dialog.buttonBox.accepted.connect(lambda: self.load_image_on_canvas())
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
                brush = QBrush(QColor(255, 20, 147))

                mid_x = int((top_left[0] + bottom_right[0]) / 4)
                mid_y = int((top_left[1] + bottom_right[1]) / 4)

                # scene.addEllipse(mid_x, mid_y, 10, 10, color, brush)
                self.center_point = QGraphicsEllipseItem(mid_x, mid_y, 10, 10);
                self.center_point.setPen(color)
                self.center_point.setBrush(brush)
                scene.addItem(self.center_point)
                scene.removeItem(self.model_item)
                scene.removeItem(self.search_item)

    def load_image_on_canvas(self):
        self.scene = QGraphicsScene()
        w = self.ui.graphicsView.size().width()
        h = self.ui.graphicsView.size().height()
        self.scene.setSceneRect(0, 0, w, h)
        pic = QtGui.QPixmap("D://Vision_Application//hul_bad_230219\Bad//Image00114.BMP")
        pic2 = pic.scaled(w, h, Qt.IgnoreAspectRatio, Qt.FastTransformation)

        # pic = pic.scaledToWidth(w, Qt.FastTransformation).scaledToHeight(h, Qt.FastTransformation)
        self.scene.addPixmap(pic2)
        self.ui.graphicsView.setScene(self.scene)
        self.scene.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
