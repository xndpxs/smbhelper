from PySide6.QtWidgets import QMainWindow, QMessageBox
from ui_smbhelper import Ui_SMBWindow
from pathlib import Path
from pwd import getpwnam
import os


class SmbHelper(QMainWindow, Ui_SMBWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app

        self.button_apply.clicked.connect(self.apply_clicked)

        self.button_cancel.clicked.connect(self.close_clicked)

        self.actionQuit.triggered.connect(self.close_clicked)

    def close_clicked(self):
        self.app.quit()

    def apply_clicked(self):
        """Events when accept button is pushed"""
        self.button_apply.setEnabled(False)
        self.text_edit.append("button clicked")

        ###############ATTRIBUTES##################################################
        self.samba_ip = self.line_samba_ip.text()
        self.samba_share = self.line_samba_share.text()
        self.samba_user = self.line_samba_user.text()
        self.samba_pass = self.line_samba_pass.text()
        self.samba_domain = self.line_samba_domain.text()
        self.samba_path = self.line_local_folder.text()
        # Dependent atributes
        self.credentials_filename = self.samba_ip + "_credentials"
        self.fstab_location = "/etc/fstab"
        self.samba_path_credentials = "/etc/samba/credentials"
        self.credentials_filepath = (
            self.samba_path_credentials + "/" + self.credentials_filename
        )
        self.uid = getpwnam(f"{self.samba_user}").pw_uid
        self.gid = getpwnam(f"{self.samba_user}").pw_gid
        self.fstab_entry = f"//{self.samba_ip}/{self.samba_share} {self.samba_path} cifs rw,x-systemd.automount,credentials={self.credentials_filepath}, uid={self.uid},gid={self.gid} 0 0"
        ############################################################################

        # # Debugging
        # self.text_edit.append(f"Samba IP: {self.samba_ip}")
        # self.text_edit.append(f"Samba share: {self.samba_share}")
        # self.text_edit.append(f"Samba user: {self.samba_user}")
        # self.text_edit.append(f"Samba pass: {self.samba_pass}")
        # self.text_edit.append(f"Samba domain: {self.samba_domain}")
        # self.text_edit.append(f"Local folder: {self.samba_path}")
        # self.text_edit.append(f"Credentials filename:  {self.credentials_filename}")
        # self.text_edit.append(f"Fstab location:  {self.fstab_location}")
        # self.text_edit.append(
        #     f"Samba path credentials:   {self.samba_path_credentials}"
        # )
        # self.text_edit.append(f"Credentials filepath:    {self.credentials_filepath}")
        # ###

        # Call the functions to create the samba share
        self.check_credentials_folder()
        self.check_credentials_file()
        self.fstab_modify()
        self.fstab_validation()

    ###########################CREDENTIALS#####################################################
    def check_credentials_folder(self):
        if Path(self.samba_path_credentials).exists():
            self.text_edit.append("Folder for credentials already found. Using it...\n")
        else:
            self.text_edit.append("Folder not found, creating one...\n")
            self.create_credentials_folder()

    def create_credentials_folder(self):
        Path(self.samba_path_credentials).mkdir(0o700, exist_ok=True)
        self.text_edit.append("Folder for credentials created...\n")

    ##################################### File
    def check_credentials_file(self):
        if Path(self.credentials_filepath).exists():
            self.msg_overwrite_credentials_file()
        else:
            self.write_credentials_file()

    def msg_overwrite_credentials_file(self):
        msg_credentials = QMessageBox.warning(
            self,
            "Overwrite Credentials File",
            "File already exists. Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if msg_credentials == QMessageBox.Yes:
            self.write_credentials_file()
        else:
            self.text_edit.append("Credentials file not overwritten...")

    def write_credentials_file(self):
        self.text_edit.append("Writing credentials...\n")
        with open(Path(self.credentials_filepath), "w", 0o600) as file:
            file.write(f"username={self.samba_user}\n")
            file.write(f"password={self.samba_pass}\n")
            file.write(f"domain={self.samba_domain}\n")
        self.text_edit.append(" Credentials file Written...")

    ################################FSTAB#####################################
    # ------------------------FSTAB TEMP FILE---------------------------------
    def fstab_create_temp(self):
        fstab_tmp = self.fstab_read()
        with open("fstab.bak", "w+") as file:
            file.write(fstab_tmp)
        self.text_edit.append("Fstab temp created...\n")

    def fstab_delete_temp(self):
        os.remove("fstab.bak")
        self.text_edit.append("Fstab temp deleted...")
        self.button_apply.setEnabled(True)

    # ---------------------------MODIFYING FSTAB----------------------------------

    def fstab_read(self):
        self.text_edit.append("Reading fstab...\n")
        with open(f"{self.fstab_location}", "r") as file:
            return file.read()

    def fstab_print(self):
        self.text_edit.append("Printing fstab...\n")
        print(self.fstab_read())

    def fstab_readlines(self):
        self.text_edit.append("Reading fstab...\n")
        with open(f"{self.fstab_location}", "r") as f:
            return f.readlines()

    def fstab_append(self, content):
        self.text_edit.append("Appending to fstab...")
        with open(f"{self.fstab_location}", "a") as file:
            file.write(content)

    def fstab_modify(self):
        self.text_edit.append("Modifying fstab...\n")
        self.fstab_create_temp()
        lines = self.fstab_readlines()
        # self.text_edit.append(f"lines: {lines}\n") # debug
        # self.text_edit.append(self.fstab_entry.strip()) # debug
        if any(line.strip() == self.fstab_entry.strip() for line in lines):
            self.text_edit.append(
                f"A line in /etc/fstab for {self.fstab_entry} already exists. New entry not added."
            )
        else:
            self.text_edit.append(self.fstab_entry.strip())
            self.fstab_append(self.fstab_entry)
            self.fstab_print()

    # # ----------------------SHARE FOLDER CHECK-----------------------------
    def path_share(self):
        return Path(self.samba_share)

    def check_folder_share(self):
        print(f"share file: {self.path_share()}")  # d

        if self.path_share().exists():
            self.text_edit.append("Folder for mount already found. Using it...\n")
        else:
            self.text_edit.append("Folder not found, creating one...\n")
            self.create_folder()

    def create_folder(self):
        self.path_share().mkdir()
        self.text_edit.append("Folder created...\n")
        try:
            os.chown(self.path_share(), self.uid, self.gid)
            self.text_edit.append("Folder permissions added...\n")
        except KeyError as e:
            self.text_edit.append(
                f"Error: User or group '{self.samba_user}' not found.\n"
            )
            self.text_edit.append(f"{e}")

    # # ---------------------VALIDATING FSTAB---------------------------------

    def fstab_validation(self):
        self.text_edit.append("Validating fstab...\n")
        try:
            os.system("systemctl daemon-reload")
            os.system("mount -a")
            self.text_edit.append(
                "Fstab validation successful, enjoy your mount :D...\n"
            )
        except OSError as e:
            self.text_edit.append("Fstab validation failed...\n")
            self.text_edit.append(f"{e}\n")
            self.text_edit.append(
                "Please not restart and manually verify /etc/fstab!\n"
            )

    # # --------------------------RETURN TO BEGINNING IF ERROR----------------------

    def delete_created_files(self):
        self.text_edit.append("Returning to last valid configuration...\n")
        if Path(self.credentials_filepath):
            Path.unlink(Path(self.credentials_filepath))
            self.text_edit.append("Credentials file deleted...\n")
        if Path(self.credentials_filepath):
            Path.unlink(Path(self.credentials_filepath))
            self.text_edit.append("Credentials file deleted...\n")

    def restore_fstab(self):
        self.text_edit.append("Restoring fstab...\n")
        lines = self.fstab_read()
        with open(f"{self.fstab_location}", "w") as f:
            for line in lines:
                if not line.startswith(self.fstab_location):
                    f.write(line)
            print("Removed entry from /etc/fstab.\n")
