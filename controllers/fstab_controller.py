import os
import shutil
import subprocess
from pathlib import Path
from pwd import getpwnam


class FstabController:
    """Class that handles modifications to the /etc/fstab file and related operations."""

    def __init__(self, text_edit):
        """
        Initializes the fstab controller.

        :param text_edit: Reference to the QTextEdit widget for displaying messages to the user.
        """
        self.text_edit = text_edit

    def prepare_fstab_entry(self, config_data):
        """
        Obtains UID and GID and constructs the /etc/fstab entry.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if prepared successfully, False otherwise.
        """
        try:
            if not config_data.samba_user:
                self.text_edit.append("Samba user is not specified.")
                return False

            user_info = getpwnam(config_data.samba_user)
            config_data.uid = user_info.pw_uid
            config_data.gid = user_info.pw_gid
            config_data.fstab_entry = (
                f"//{config_data.samba_ip}/{config_data.samba_share} "
                f"{config_data.samba_path} cifs "
                f"rw,x-systemd.automount,credentials={config_data.credentials_filepath},"
                f"uid={config_data.uid},gid={config_data.gid} 0 0"
            )
            return True
        except KeyError:
            self.text_edit.append(
                f"User '{config_data.samba_user}' does not exist on this system."
            )
            return False
        except Exception as e:
            self.text_edit.append(f"Error retrieving UID and GID: {e}")
            return False

    def modify_fstab(self, config_data):
        """
        Modifies the /etc/fstab file to add the shared resource entry.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if modified successfully, False otherwise.
        """
        try:
            if not self.create_backup(config_data):
                return False
            if self.entry_exists(config_data):
                self.text_edit.append("Fstab entry already exists. Skipping.")
                return True
            else:
                if self.append_entry(config_data):
                    return True
                else:
                    return False
        except PermissionError:
            self.text_edit.append("Permission denied. Please run the program as root.")
            return False
        except Exception as e:
            self.text_edit.append(f"Error modifying fstab: {e}")
            return False

    def create_backup(self, config_data):
        """
        Creates a backup of the /etc/fstab file.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if backup created successfully, False otherwise.
        """
        try:
            fstab_path = Path(config_data.fstab_location)
            backup_path = fstab_path.with_suffix(".bak")
            shutil.copyfile(fstab_path, backup_path)
            self.text_edit.append("Fstab backup created.")
            return True
        except Exception as e:
            self.text_edit.append(f"Failed to create fstab backup: {e}")
            return False

    def entry_exists(self, config_data):
        """
        Checks if the entry already exists in /etc/fstab.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the entry exists, False otherwise.
        """
        try:
            with open(config_data.fstab_location, "r") as f:
                entries = f.read()
            return config_data.fstab_entry.strip() in entries
        except Exception as e:
            self.text_edit.append(f"Failed to read fstab: {e}")
            return False

    def append_entry(self, config_data):
        """
        Appends the entry to the /etc/fstab file.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the entry was appended successfully, False otherwise.
        """
        try:
            with open(config_data.fstab_location, "a") as f:
                f.write(config_data.fstab_entry + "\n")
            self.text_edit.append("Fstab entry added.")
            return True
        except Exception as e:
            self.text_edit.append(f"Failed to append fstab entry: {e}")
            return False

    def create_mount_point(self, config_data):
        """
        Creates the mount point if it does not exist.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the mount point is created or already exists, False otherwise.
        """
        mount_point = Path(config_data.samba_path)
        if not mount_point.exists():
            try:
                mount_point.mkdir(parents=True)
                self.text_edit.append(
                    f"Created mount point at {config_data.samba_path}."
                )
                config_data.mount_point_created = True
                return True
            except Exception as e:
                self.text_edit.append(f"Failed to create mount point: {e}")
                return False
        else:
            self.text_edit.append("Mount point already exists.")
            return True

    def validate_and_mount(self, config_data):
        """
        Attempts to mount the shared resource to validate the configuration.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the mount is successful, False otherwise.
        """
        try:
            self.text_edit.append("Attempting to mount the share...")
            # Mount the shared resource
            subprocess.run(["mount", config_data.samba_path], check=True)
            self.text_edit.append("Mount successful.")

            # Unmount the shared resource (optional)
            subprocess.run(["umount", config_data.samba_path], check=True)
            self.text_edit.append("Unmounted the share after validation.")
            return True
        except subprocess.CalledProcessError as e:
            self.text_edit.append(f"Mount failed: {e}")
            return False

    def cleanup_changes(self, config_data):
        """
        Performs cleanup of the changes made.

        :param config_data: Instance of ConfigData containing configuration data.
        """
        self.cleanup_credentials_file(config_data)
        self.remove_fstab_entry(config_data)
        self.delete_mount_point(config_data)

    def cleanup_credentials_file(self, config_data):
        """
        Deletes the credentials file.

        :param config_data: Instance of ConfigData containing configuration data.
        """
        credentials_file = Path(config_data.credentials_filepath)
        if credentials_file.exists():
            try:
                credentials_file.unlink()
                self.text_edit.append("Credentials file deleted.")
            except Exception as e:
                self.text_edit.append(f"Failed to delete credentials file: {e}")

    def remove_fstab_entry(self, config_data):
        """
        Removes the added entry from /etc/fstab.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the entry was removed successfully, False otherwise.
        """
        try:
            with open(config_data.fstab_location, "r") as f:
                lines = f.readlines()
            with open(config_data.fstab_location, "w") as f:
                for line in lines:
                    if line.strip() != config_data.fstab_entry.strip():
                        f.write(line)
            self.text_edit.append("Removed the fstab entry.")
            return True
        except Exception as e:
            self.text_edit.append(f"Failed to remove fstab entry: {e}")
            return False

    def delete_mount_point(self, config_data):
        """
        Deletes the mount point if it was created by the program.

        :param config_data: Instance of ConfigData containing configuration data.
        :return: True if the mount point was deleted successfully, False otherwise.
        """
        if config_data.mount_point_created:
            mount_point = Path(config_data.samba_path)
            try:
                mount_point.rmdir()
                self.text_edit.append(
                    f"Deleted mount point at {config_data.samba_path}."
                )
                return True
            except Exception as e:
                self.text_edit.append(f"Failed to delete mount point: {e}")
                return False
