import sys

from PySide2 import QtGui
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView

from gui.ui_mainwindow import Ui_MainWindow
from setup_image import SetupImageDialog
from draggable_resizable_rectangle import GraphicsRectItem


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_29.clicked.connect(lambda: self.load_image())
        self.ui.pushButton_31.clicked.connect(lambda: self.createGraphicView())
        self.ui.statusbar.addPermanentWidget(self.ui.progressBar)

        self.createGraphicView()

    def load_image(self):
        self.setupimage = SetupImageDialog()
        self.setupimage.setWindowModality(Qt.ApplicationModal)
        self.setupimage.dialog.buttonBox.accepted.connect(lambda: self.load_image_on_canvas())
        self.setupimage.exec_()

    def createGraphicView(self):
        # get selected tool
        getSelected = self.ui.treeWidget_2.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            if (getChildNode == 'Patterns'):
                # self.ui.graphicsView.
                scene = self.ui.graphicsView.scene()
                if scene is None:
                    scene = QGraphicsScene()
                w = self.ui.graphicsView.size().width()
                h = self.ui.graphicsView.size().height()
                self.scene.setSceneRect(0, 0, w, h)
                self.ui.graphicsView.setScene(scene)
                search_item = GraphicsRectItem(50, 50, 200, 200, color=Qt.green, status_bar=self.ui.statusbar)
                scene.addItem(search_item)
                model_item = GraphicsRectItem(100, 100, 100, 100, color=Qt.red, status_bar=self.ui.statusbar)
                scene.addItem(model_item)

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
