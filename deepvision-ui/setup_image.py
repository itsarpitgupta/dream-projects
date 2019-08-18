from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from gui.ui_loadimage import Ui_Dialog

class SetupImageDialog(QDialog):

    def __init__(self):
        super(SetupImageDialog, self).__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
