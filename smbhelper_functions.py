from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from ui_smbhelper import Ui_SMBWindow
import os
class SmbHelper(QMainWindow, Ui_SMBWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.button_apply.clicked.connect(self.apply_clicked)
        self.button_cancel.clicked.connect(self.close_clicked)


        
        
        


    def apply_clicked(self):
        print("Apply Clicked")

    def close_clicked(self, event):
        self.app.quit()

# -----------------FOLDER CREATION-----------------------------------
# Create the credentials folder in specified path
def create_credentials_folder(path_credentials):
    if os.path.exists(path_credentials):
        print(" Folder for credentials already found. Using it...")
    else:
        try:
            print(" Folder not found, creating one...")
            os.makedirs(path_credentials, 0o700, exist_ok=True)
            print(" Folder for credentials created...")
        except Exception as error:
            print(f" Can't create credentials folder: {error}")