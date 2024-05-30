from pathlib import Path
import os


class FstabConfig:
    def __init__(self, sf):
        # INSTANCES
        self.sf = sf

    # METHODS
    def fstab_create_temp(self):
        with open(f"{self.sf.fstab_location}", "r") as file:
            fstab_data = file.read()
        with open("fstab.bak", "w+") as file:
            file.write(fstab_data)
        self.sf.text_edit.append("Fstab temsfcreated...")

    def fstab_delete_temp(self):
        os.remove("fstab.bak")
        self.sf.text_edit.append("Fstab temp deleted...")
        self.sf.button_apply.setEnabled(True)

    def fstab_modify(self):
        self.sf.text_edit.append("Modifying fstab...")
        self.fstab_create_temp()
        with open(f"{self.sf.fstab_location}", "r") as f:
            lines = f.readlines()
            if any(line.strip() == self.sf.fstab_entry.strip() for line in lines):
                self.sf.text_edit.append(
                    f"A line for {self.sf.fstab_entry} already exists. New entry not added."
                )
            else:
                self.sf.text_edit.append("Appending to fstab...")
                with open(f"{self.sf.fstab_location}", "a") as file:
                    file.write(self.sf.fstab_entry.strip())

    def fstab_validation(self):
        self.sf.text_edit.append("Validating fstab...")
        try:
            os.system("systemctl daemon-reload")
            os.system("mount -a")
            self.sf.text_edit.append(
                "Fstab validation successful, enjoy your mount :D...\n"
            )
        except OSError as e:
            self.sf.text_edit.append("Fstab validation failed...")
            self.sf.text_edit.append(f"{e}")
            self.sf.text_edit.append(
                "Please not restart and manually verify /etc/fstab!"
            )

    def restore_fstab(self):
        self.sf.text_edit.append("Restoring fstab...")
        with open(f"{self.sf.fstab_location}", "r") as f:
            lines = f.readlines()
        with open(f"{self.sf.fstab_location}", "w") as f:
            for line in lines:
                if not line.startswith(self.sf.fstab_location):
                    f.write(line)
            print("Removed entry from /etc/fstab.")

    def create_share_folder(self):
        if Path(self.sf.samba_share).exists():
            self.sf.text_edit.append("Folder for mount already found. Using it...")
        else:
            Path(self.sf.samba_share).mkdir()
            self.sf.text_edit.append("Folder created...")
            try:
                os.chown(
                    Path(self.sf.samba_share),
                    self.sf.uid,
                    self.sf.gid,
                )
                self.sf.text_edit.append("Folder permissions added...\n")
            except KeyError as e:
                self.sf.text_edit.append(
                    f"Error: User or group '{self.sf.samba_user}' not found.\n"
                )
                self.sf.text_edit.append(f"{e}")
