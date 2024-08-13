from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication
from smbfunctions.samba_config import SambaConfig
from smbfunctions.fstab_config import FstabConfig
from ui.ui_smbwindow import Ui_SMBWindow
from pwd import getpwnam


class SmbHelper(QMainWindow, Ui_SMBWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        # VARIABLES
        self.app = app
        self.samba_config = SambaConfig(self)
        self.fstab_config = FstabConfig(self)

        # SLOTS
        self.button_apply.clicked.connect(self.apply_clicked)
        self.button_cancel.clicked.connect(self.close_clicked)
        self.actionQuit.triggered.connect(self.close_clicked)
        self.button_search.clicked.connect(self.folder_search)

    # METHODS
    def close_clicked(self):
        self.app.quit()

    def apply_clicked(self):
        self.button_apply.setEnabled(False)
        self.text_edit.append("button clicked...")
        QApplication.processEvents()
        self.get_variables()
        if self.get_uid_gid():
            self.samba_config.create_credentials_folder()
            QApplication.processEvents()
            self.samba_config.create_credentials_file()
            QApplication.processEvents()
            self.fstab_config.fstab_modify()
            QApplication.processEvents()
        else:
            self.button_apply.setEnabled(True)

        # if not self.fstab_config.fstab_validation():
        #     QApplication.processEvents()
        #     self.samba_config.delete_created_files()
        #     QApplication.processEvents()
        # self.button_apply.setEnabled(True)

        # FUNCTIONS

    def get_variables(self):
        # VARIABLES
        self.samba_ip = self.line_samba_ip.text()
        self.samba_share = self.line_samba_share.text()
        self.samba_user = self.line_samba_user.text()
        self.samba_pass = self.line_samba_pass.text()
        self.samba_domain = self.line_samba_domain.text()
        self.samba_path = self.line_local_folder.text()

        # DEPENDENT VARIABLES
        self.samba_path_credentials = "/etc/samba/credentials"
        self.credentials_filename = self.samba_ip + "_credentials"
        self.credentials_filepath = (
            self.samba_path_credentials + "/" + self.credentials_filename
        )

        # FSTAB VARIABLES
        self.fstab_location = "/etc/fstab"

    def get_uid_gid(self):
        try:
            self.uid = getpwnam(self.samba_user).pw_uid
            self.gid = getpwnam(self.samba_user).pw_gid
            self.fstab_entry = f"//{self.samba_ip}/{self.samba_share} {self.samba_path} cifs rw,x-systemd.automount,credentials={self.credentials_filepath},uid={self.uid},gid={self.gid} 0 0\n"
            return True
        except KeyError:
            self.text_edit.append(
                f"User {self.samba_user} does not exist. Program ended."
            )
            self.button_apply.setEnabled(True)
            return False

    def folder_search(self):
        self.samba_path = QFileDialog().getExistingDirectory()
        self.line_local_folder.setText(self.samba_path)
