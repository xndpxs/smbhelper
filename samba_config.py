from PySide6.QtWidgets import QMessageBox
from ui_smbwindow import Ui_SMBWindow
from pathlib import Path
from pwd import getpwnam


class SambaConfig:
    def __init__(self):
        super().__init__()

        # INSTANCE
        self.ui = Ui_SMBWindow()

    # FUNCTIONS
    def get_variables(self):
        # VARIABLES
        self.samba_ip = self.ui.line_samba_ip.text()
        self.samba_share = self.ui.line_samba_share.text()
        self.samba_user = self.ui.line_samba_user.text()
        self.samba_pass = self.ui.line_samba_pass.text()
        self.samba_domain = self.ui.line_samba_domain.text()
        self.samba_path = self.ui.line_local_folder.text()

        # DEPENDENT VARIABLES
        self.samba_path_credentials = "/etc/samba/credentials"
        self.credentials_filename = self.samba_ip + "_credentials"
        self.credentials_filepath = (
            self.samba_path_credentials + "/" + self.credentials_filename
        )

        # FSTAB VARIABLES
        self.fstab_location = "/etc/fstab"
        self.fstab_entry = f"//{self.samba_ip}/{self.samba_share} {self.samba_path} cifs rw,x-systemd.automount,credentials={self.samba_path_credentials},uid={self.uid},gid={self.gid} 0 0"

    def get_uid_gid(self):
        try:
            self.uid = getpwnam(f"{self.samba_user}").pw_uid
            self.gid = getpwnam(f"{self.samba_user}").pw_gid
        except KeyError as e:
            self.ui.text_edit.append(f"User {e} does not exist. Program ended.")
            self.ui.button_apply.setEnabled(True)

    # Folder credentials creation
    def create_credentials_folder(self):
        if Path(self.samba_path_credentials).exists():
            self.ui.text_edit.append(
                "Folder for credentials already found. Using it..."
            )
        else:
            self.ui.text_edit.append("Folder not found, creating one...")
            Path(self.samba_path_credentials).mkdir(0o700, exist_ok=True)
            self.ui.text_edit.append("Folder for credentials created...")

    # File credentials creation
    def create_credentials_file(self):
        if Path(self.credentials_filepath).exists():
            self.msg_overwrite_credentials_file(self)
        else:
            self.ui.text_edit.append("Writing credentials...\n")
            with open(Path(self.credentials_filepath), "w", 0o600) as file:
                file.write(f"username={self.samba_user}\n")
                file.write(f"password={self.samba_pass}\n")
                file.write(f"domain={self.samba_domain}\n")
            self.ui.text_edit.append(" Credentials file Written...")

    def msg_overwrite_credentials_file(self, parent):
        msg_credentials = QMessageBox.warning(
            parent,
            "Overwrite Credentials File",
            "File already exists. Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if msg_credentials == QMessageBox.Yes:
            self.create_credentials_file()
        else:
            self.ui.text_edit.append("Credentials file not overwritten...")

    def delete_created_files(self):
        self.ui.text_edit.append("Returning to last valid configuration...")
        if Path(self.credentials_filepath):
            Path.unlink(Path(self.credentials_filepath))
            self.ui.text_edit.append("Credentials file deleted...")
