import sys

from PyQt5 import QtCore
from PySide2.QtWidgets import QApplication, QMainWindow, QAction

from get_connection import get_connection_click_event
from gui.ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(0))
        # self.ui.pushButton.clicked.connect(lambda : get_connection_click_event(self.ui.stackedWidget))
        self.ui.pushButton_2.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.statusbar.addPermanentWidget(self.ui.progressBar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())