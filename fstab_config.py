from pathlib import Path
import subprocess
import os
import shutil


class FstabConfig:
    def __init__(self, sf):
        # INSTANCES
        self.sf = sf

    # METHODS
    def fstab_create_temp(self):
        try:
            shutil.copyfile("/etc/fstab", "/etc/fstab.bak")
            self.sf.text_edit.append("Fstab backup created...")
        except FileNotFoundError as e:
            self.sf.text_edit.append("No /etc/fstab file found.")
        except IOError as e:
            self.sf.text_edit.append(f"Failed to create temporary backup of fstab: {e}")

    def fstab_delete_temp(self):
        try:
            Path("/etc/fstab.bak").unlink()
            self.sf.text_edit.append("Fstab temp deleted...")
            self.sf.button_apply.setEnabled(True)
        except FileNotFoundError as e:
            self.sf.text_edit.append("No backup found...")
        except OSError as e:
            self.sf.text_edit.append("Failed to delete backup of fstab: {e}")

    def fstab_modify(self):
        try:
            self.sf.text_edit.append("Modifying fstab...")
            self.fstab_create_temp()

            with open(self.sf.fstab_location, "r") as f:
                lines = f.readlines()
                if any(line.strip() == self.sf.fstab_entry.strip() for line in lines):
                    self.sf.text_edit.append(
                        f"A line for {self.sf.fstab_entry} already exists. New entry not added."
                    )
                else:
                    self.sf.text_edit.append("Appending to fstab...")
                    with open(self.sf.fstab_location, "a") as file:
                        file.write(self.sf.fstab_entry.strip())
        except FileNotFoundError:
            self.sf.text_edit.append(f"Error: {self.sf.fstab_location} not found.")
        except IOError as e:
            self.sf.text_edit.append(f"IOError occurred while modifying fstab: {e}")

    def fstab_validation(self):
        self.sf.text_edit.append("Validating fstab...")

        try:
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["mount", "-a"], check=True)
            self.sf.text_edit.append(
                "Fstab validation successful, enjoy your mount :D..."
            )
            return True

        except subprocess.CalledProcessError as e:
            self.sf.text_edit.append("Fstab validation failed...")
            self.sf.text_edit.append(f"Error: {e}")
            self.sf.text_edit.append("Restoring fstab...")
            self.restore_fstab()
            self.sf.text_edit.append(
                "Please manually verify /etc/fstab before restart the computer"
            )
            return False

    def restore_fstab(self):
        backup_path = Path(f"{self.sf.fstab_location}.bak")
        fstab_path = Path(self.sf.fstab_location)

        if not backup_path.exists():
            self.sf.text_edit.append(f"Backup file {backup_path} not found.")
            return

        try:
            shutil.copy(backup_path, fstab_path)
            self.sf.text_edit.append("Restored the backup of fstab from fstab.bak")
        except IOError as e:
            self.sf.text_edit.append(f"Failed to restore the backup of fstab: {e}")

    def create_share_folder(self):
        share_path = Path(self.sf.samba_share)

        if share_path.exists():
            self.sf.text_edit.append("Folder for mount already found. Using it...")
        else:
            share_path.mkdir(parents=True, exist_ok=True)
            self.sf.text_edit.append("Folder created...")

            try:
                os.chown(share_path, self.sf.uid, self.sf.gid)
                self.sf.text_edit.append("Folder permissions added...")
            except KeyError as e:
                self.sf.text_edit.append(
                    f"Error: User or group '{self.sf.samba_user}' not found."
                )
                self.sf.text_edit.append(f"Error:{e}")
