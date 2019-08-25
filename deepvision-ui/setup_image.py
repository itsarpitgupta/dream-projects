from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QFileDialog
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

    def open_folder_browser(self):
        widget = FileBrowser()
        widget.setWindowModality(Qt.ApplicationModal)
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.dialog.comboBox.addItem(file)
        onlyfiles = next(os.walk(file))[2]  # dir is your directory path as string
        self.dialog.lineEdit.setText(str(len(onlyfiles)))
