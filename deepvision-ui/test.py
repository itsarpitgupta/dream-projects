import sys

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QAction
from gui.ui_mainwindow import Ui_MainWindow
from setup_image import SetupImageDialog
import numpy as np
import random


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_17.clicked.connect(lambda: self.load_image())
        self.ui.pushButton_16.clicked.connect(lambda: self.update_graph())
        self.ui.statusbar.addPermanentWidget(self.ui.progressBar)

    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.ui.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.ui.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.ui.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signals')
        self.ui.MplWidget.canvas.draw()

    def load_image(self):
        dialog = SetupImageDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
