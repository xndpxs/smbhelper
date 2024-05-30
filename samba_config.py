from PySide6.QtWidgets import QMessageBox
from pathlib import Path


class SambaConfig:
    def __init__(self, sf):
        # INSTANCE
        self.sf = sf

    # Folder credentials creation
    def create_credentials_folder(self):
        if Path(self.sf.samba_path_credentials).exists():
            self.sf.text_edit.append(
                "Folder for credentials already found. Using it..."
            )
        else:
            self.sf.text_edit.append("Folder not found, creating one...")
            Path(self.sf.samba_path_credentials).mkdir(0o700, exist_ok=True)
            self.sf.text_edit.append("Folder for credentials created...")

    # File credentials creation
    def msg_overwrite_credentials_file(self, parent):
        msg_credentials = QMessageBox.warning(
            parent,
            "Overwrite Credentials File",
            "File for credentials already exists. Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if msg_credentials == QMessageBox.Yes:
            self.create_credentials_file()
        else:
            self.sf.text_edit.append("Credentials file not overwritten...")

    def create_credentials_file(self):
        if Path(self.sf.credentials_filepath).exists():
            self.msg_overwrite_credentials_file(self.sf)
        else:
            self.sf.text_edit.append("Writing credentials...\n")
            with open(Path(self.sf.credentials_filepath), "w", 0o600) as file:
                file.write(f"username={self.sf.samba_user}\n")
                file.write(f"password={self.sf.samba_pass}\n")
                file.write(f"domain={self.sf.samba_domain}\n")
            self.sf.text_edit.append(" Credentials file Written...")

    def delete_created_files(self):
        self.sf.text_edit.append("Returning to last valid configuration...")
        if Path(self.sf.credentials_filepath):
            Path.unlink(Path(self.sf.credentials_filepath))
            self.sf.text_edit.append("Credentials file deleted...")
