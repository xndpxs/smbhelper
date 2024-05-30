from samba_config import SambaConfig
from ui_smbwindow import Ui_SMBWindow
from pathlib import Path
import os


class FstabConfig:
    def __init__(self):
        super().__init__()

        # INSTANCES
        self.ui = Ui_SMBWindow()
        self.samba_config = SambaConfig()

        # VARIABLES

    # METHODS

    def fstab_create_temp(self):
        with open(f"{self.samba_config.fstab_location}", "r") as file:
            fstab_data = file.read()
        with open("fstab.bak", "w+") as file:
            file.write(fstab_data)
        self.ui.text_edit.append("Fstab temp created...")

    def fstab_delete_temp(self):
        os.remove("fstab.bak")
        self.ui.text_edit.append("Fstab temp deleted...")
        self.ui.button_apply.setEnabled(True)

    def fstab_modify(self):
        self.ui.text_edit.append("Modifying fstab...")
        self.fstab_create_temp()
        with open(f"{self.samba_config.fstab_location}", "r") as f:
            lines = f.readlines()
            if any(
                line.strip() == self.samba_config.fstab_entry.strip() for line in lines
            ):
                self.ui.text_edit.append(
                    f"A line for {self.samba_config.fstab_entry} already exists. New entry not added."
                )
            else:
                self.ui.text_edit.append("Appending to fstab...")
                with open(f"{self.samba_config.fstab_location}", "a") as file:
                    file.write(self.samba_config.fstab_entry.strip())

    def fstab_validation(self):
        self.ui.text_edit.append("Validating fstab...")
        try:
            os.system("systemctl daemon-reload")
            os.system("mount -a")
            self.ui.text_edit.append(
                "Fstab validation successful, enjoy your mount :D...\n"
            )
        except OSError as e:
            self.ui.text_edit.append("Fstab validation failed...")
            self.ui.text_edit.append(f"{e}")
            self.ui.text_edit.append(
                "Please not restart and manually verify /etc/fstab!"
            )

    def restore_fstab(self):
        self.ui.text_edit.append("Restoring fstab...")
        with open(f"{self.samba_config.fstab_location}", "r") as f:
            lines = f.readlines()
        with open(f"{self.samba_config.fstab_location}", "w") as f:
            for line in lines:
                if not line.startswith(self.samba_config.fstab_location):
                    f.write(line)
            print("Removed entry from /etc/fstab.")

    def create_share_folder(self):
        if Path(self.samba_config.samba_share).exists():
            self.ui.text_edit.append("Folder for mount already found. Using it...\n")
        else:
            Path(self.samba_config.samba_share).mkdir()
            self.ui.text_edit.append("Folder created...\n")
            try:
                os.chown(
                    Path(self.samba_config.samba_share),
                    self.samba_config.uid,
                    self.samba_config.gid,
                )
                self.ui.text_edit.append("Folder permissions added...\n")
            except KeyError as e:
                self.ui.text_edit.append(
                    f"Error: User or group '{self.samba_config.samba_user}' not found.\n"
                )
                self.ui.text_edit.append(f"{e}")
