from PySide2.QtCore import Qt, QRectF
from PySide2.QtWidgets import QDialog, QFileDialog, QGraphicsScene
import os, os.path
from gui.ui_loadimage import Ui_Dialog
from setup_image_file_browser import FileBrowser


class SetupImageDialog(QDialog):

    def __init__(self):
        super(SetupImageDialog, self).__init__()
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
        self.dialog.radioButton.setChecked(True)
        self.dialog.toolButton.clicked.connect(lambda: self.open_folder_browser())
        self.dialog.buttonBox.rejected.connect(self.reject)

    def open_folder_browser(self):
        widget = FileBrowser()
        widget.setWindowModality(Qt.ApplicationModal)
        self.file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dialog.comboBox.addItem(self.file)
        onlyfiles = next(os.walk(self.file))[2]  # dir is your directory path as string
        self.dialog.lineEdit.setText(str(len(onlyfiles)))
