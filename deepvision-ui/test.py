import sys

from PySide2.QtGui import Qt, QBrush, QPen, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsScene, QGraphicsView, QGraphicsItem

from rectangle_scene import PatternToolScene
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
        self.ui.statusbar.addPermanentWidget(self.ui.progressBar)

        self.createGraphicView()

    def load_image(self):
        dialog = SetupImageDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def createGraphicView(self):
        # self.patternScene = PatternToolScene(self)
        # self.ui.graphicsView.setScene(self.patternScene)


        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 400, 400)

        self.ui.graphicsView.setScene(scene)

        search_item = GraphicsRectItem(0, 0, 200, 200 , color = Qt.green)
        scene.addItem(search_item)

        model_item = GraphicsRectItem(50, 50, 100, 100, color = Qt.red)
        scene.addItem(model_item)

        # self.ui.graphicsView.show()
        # sys.exit(app.exec_())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
