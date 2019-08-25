
from PySide2.QtGui import Qt, QBrush, QPen, QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsScene, QGraphicsView, QGraphicsItem, \
    QGraphicsItemGroup
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QGraphicsScene


class PatternToolScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.shapes()

    # def mousePressEvent(self, event):
    #    print("mouser event")

    def shapes(self):
        self.pen_green = QPen(Qt.green)
        # self.pen_green.setStyle(Qt.DotLine)
        self.pen_pink = QPen(QColor(204, 123, 25))

        self.search_grp = QGraphicsItemGroup(scene=self)
        self.search_grp.setFlag(QGraphicsItem.ItemIsMovable)
        self.search_grp.setFlag(QGraphicsItem.ItemIsSelectable)
        self.search = self.addRect(-100, -100, 200, 200, self.pen_green)
        self.drawSelectMarkers(self.search_grp, self.search , self.pen_green)
        self.search_grp.show()
        self.addItem(self.search_grp)

        self.model_grp = QGraphicsItemGroup(scene=self)
        self.model_grp.setFlag(QGraphicsItem.ItemIsMovable)
        self.model_grp.setFlag(QGraphicsItem.ItemIsSelectable)
        self.model = self.addRect(-50, -50, 100, 100, self.pen_pink)
        self.drawSelectMarkers(self.model_grp, self.model ,  self.pen_pink)
        self.search_grp.show()
        self.addItem(self.model_grp)

    def drawSelectMarkers(self, group, rect , pen):

        # Top-Left
        tl = self.addRect(rect.boundingRect().topLeft().x()-3,  rect.boundingRect().topLeft().y()-3, 10, 10, pen)
        # Top-Rigth
        tr = self.addRect(rect.boundingRect().topRight().x() - 5, rect.boundingRect().topRight().y() - 3, 10, 10, pen)
        # Bottom-Left
        bl = self.addRect(rect.boundingRect().bottomLeft().x() - 3, rect.boundingRect().bottomLeft().y() - 5, 10, 10, pen)
        # Bottom-Right
        br = self.addRect(rect.boundingRect().bottomRight().x() - 5, rect.boundingRect().bottomRight().y() - 5, 10, 10, pen)

        # Top-Mid
        tm = self.addRect(int((rect.boundingRect().topRight().y() - rect.boundingRect().topLeft().y())/2),  int(rect.boundingRect().topLeft().y()-5), 10, 10, pen)

        # Bottom-Mid
        bm = self.addRect(int((rect.boundingRect().bottomRight().y() - rect.boundingRect().bottomLeft().y())/2),  int(rect.boundingRect().bottomLeft().y()-5), 10, 10, pen)

        # Right-Mid
        rm = self.addRect(int(rect.boundingRect().bottomLeft().y()-5), int((rect.boundingRect().bottomLeft().y() - rect.boundingRect().bottomLeft().y())/2), 10, 10, pen)

        # Left-Mid
        lm = self.addRect(int(rect.boundingRect().topLeft().y()-5), int((rect.boundingRect().topLeft().y() - rect.boundingRect().topLeft().y())/2), 10, 10, pen)

        group.addToGroup(rect)
        group.addToGroup(tl)
        group.addToGroup(tr)
        group.addToGroup(bl)
        group.addToGroup(br)
        group.addToGroup(tm)
        group.addToGroup(bm)
        group.addToGroup(rm)
        group.addToGroup(lm)



