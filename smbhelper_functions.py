from time import process_time
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PySide6.QtCore import QEventLoop, QProcess, QTimer
from ui_smbhelper import Ui_SMBWindow
import os

class SmbHelper(QMainWindow, Ui_SMBWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        #self.messagebox = QMessageBox(self)
        

        
    ###########################################################################


        self.button_apply.clicked.connect(self.apply_clicked)

        self.button_cancel.clicked.connect(self.close_clicked)


    def apply_clicked(self):
        """Events when accept button is pushed""" 
        self.button_apply.setEnabled(False)                
        self.text_edit.append("button clicked")    

        self.samba_ip = self.line_samba_ip.text()
        self.samba_share = self.line_samba_share.text()
        self.samba_user = self.line_samba_user.text()
        self.samba_pass = self.line_samba_pass.text()
        self.samba_domain = self.line_samba_domain.text()
        self.samba_path = self.line_local_folder.text()

        self.credentials_filename = self.samba_ip + "_credentials"
        self.fstab_location = "/etc/fstab"
        self.samba_path_credentials = "/etc/samba/credentials"
        self.credentials_filepath = self.samba_path_credentials + "/" + self.credentials_filename
        
        # Debugging--------------------------------------------
        self.text_edit.append(f"Samba IP: {self.samba_ip}")
        self.text_edit.append(f"Samba share: {self.samba_share}")
        self.text_edit.append(f"Samba user: {self.samba_user}")
        self.text_edit.append(f"Samba pass: {self.samba_pass}")
        self.text_edit.append(f"Samba domain: {self.samba_domain}")
        self.text_edit.append(f"Local folder: {self.samba_path}")
        self.text_edit.append(f"Credentials filename:  {self.credentials_filename}")
        self.text_edit.append(f"Fstab location:  {self.fstab_location}")
        self.text_edit.append(f"Samba path credentials:   {self.samba_path_credentials}")
        self.text_edit.append(f"Credentials filepath:    {self.credentials_filepath}")
        #------------------------------------------------------

        # Call the functions to create the samba share
        QTimer.singleShot(1000, lambda: self.create_credentials_folder(self.samba_path_credentials))
        QTimer.singleShot(1000, lambda: self.create_credentials_file(self.samba_user, self.samba_pass, self.samba_domain, self.credentials_filepath))
        
        

    def close_clicked(self, event):
        self.app.quit()

    # -----------------FOLDER CREATION-----------------------------------
    def create_credentials_folder(self, samba_path_credentials):
        """Create the credentials folder in specified path"""
        self.text_edit.append("##########CREATING CREDENTIALS FOLDER############")
        if os.path.isdir(samba_path_credentials):            
            self.text_edit.append(" Folder for credentials already found. Using it...\n")
            self.text_edit.append("Samba path credentials = "+samba_path_credentials) # debug
        else:            
            self.text_edit.append(" Folder not found, creating one...")
            os.makedirs(samba_path_credentials, 0o700, exist_ok=True)
            self.text_edit.append(" Folder for credentials created...\n")
        #Restoring the button    
        
    
    # ----------------FILE CREDENTIALS CREATION-----------------------------
    def create_credentials_file(self, samba_user, samba_pass, samba_domain, credentials_filepath):
        """Create the file with credentials in specified path"""
        self.text_edit.append("##########CREATING CREDENTIALS FILE############")
        print("path of credentials:...", credentials_filepath)
        if os.path.isfile(credentials_filepath):
            self.message_overwrite_credentials(samba_user, samba_pass, samba_domain, credentials_filepath)
        else:
            self.text_edit.append("Can't read ")

    def message_overwrite_credentials(self, samba_user, samba_pass, samba_domain, credentials_filepath):
        """Message box to confirm overwrite"""
        print("I am in msg_credentials function...")
        msg_credentials = QMessageBox.warning(self,"Overwrite Credentials File",
            "File already exists. Do you want to overwrite it?", QMessageBox.Yes | QMessageBox.No)
        if msg_credentials == QMessageBox.Yes:
            self.write_credentials_file(samba_user, samba_pass, samba_domain, credentials_filepath)
        else:
            self.text_edit.append(" Credentials file not overwritten...")
    
    def write_credentials_file(self, samba_user, samba_pass, samba_domain, credentials_filepath):
        """Create the file with credentials in specified path"""
        with open(credentials_filepath,'w',0o600) as file:
            file.write("username="+samba_user+"\n")
            file.write("password="+samba_pass+"\n")
            file.write("domain="+samba_domain+"\n")
            self.text_edit.append(" Credentials file overwritten...")
            self.button_apply.setEnabled(True)

                    

    
