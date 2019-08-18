# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PySide2.QtWidgets import QWidget, QVBoxLayout
import matplotlib
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)