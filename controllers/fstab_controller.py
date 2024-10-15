import shutil
import subprocess
from pathlib import Path
from pyfstab import Fstab
from pwd import getpwnam


class FstabController:
    """Class that handles modifications to the /etc/fstab file and related operations."""

    def __init__(self, text_edit):
        self.text_edit = text_edit

    def prepare_fstab_entry(self, config_data):
        """Obtains UID and GID for the Samba user."""
        try:
            if not config_data.samba_user:
                self.text_edit.append("Samba user is not specified.")
                return False

            user_info = getpwnam(config_data.samba_user)
            config_data.uid = user_info.pw_uid
            config_data.gid = user_info.pw_gid
            self.text_edit.append("UID and GID obtained successfully.")
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
        """Modifies the /etc/fstab file to add the shared resource entry."""
        try:
            # Create backup
            if not self.create_backup(config_data):
                return False

            # Load existing fstab entries
            fstab = Fstab(path=config_data.fstab_location)

            # Check if the entry already exists
            if any(entry for entry in fstab if entry.fs_file == config_data.samba_path):
                self.text_edit.append("Fstab entry already exists. Skipping.")
                return True

            # Create a new fstab entry
            new_entry = fstab.create_entry()
            new_entry.fs_spec = f"//{config_data.samba_ip}/{config_data.samba_share}"
            new_entry.fs_file = config_data.samba_path
            new_entry.fs_vfstype = "cifs"
            new_entry.fs_mntops = (
                f"rw,x-systemd.automount,credentials={config_data.credentials_filepath},"
                f"uid={config_data.uid},gid={config_data.gid}"
            )
            new_entry.fs_freq = "0"
            new_entry.fs_passno = "0"

            # Add and write the new entry
            fstab.add_entry(new_entry)
            fstab.write()
            self.text_edit.append("Fstab entry added successfully.")
            return True
        except Exception as e:
            self.text_edit.append(f"Error modifying fstab: {e}")
            return False

    def create_backup(self, config_data):
        """Creates a backup of the /etc/fstab file."""
        try:
            fstab_path = Path(config_data.fstab_location)
            backup_path = fstab_path.with_suffix(".bak")
            shutil.copyfile(fstab_path, backup_path)
            self.text_edit.append("Fstab backup created.")
            return True
        except Exception as e:
            self.text_edit.append(f"Failed to create fstab backup: {e}")
            return False

    def create_mount_point(self, config_data):
        """Creates the mount point if it does not exist."""
        mount_point = Path(config_data.samba_path)
        if not mount_point.exists():
            try:
                mount_point.mkdir(parents=True, exist_ok=True)
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
            config_data.mount_point_created = False
            return True

    def validate_and_mount(self, config_data):
        """Attempts to mount the shared resource to validate the configuration."""
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
        """Performs cleanup of the changes made."""
        self.cleanup_credentials_file(config_data)
        self.remove_fstab_entry(config_data)
        self.delete_mount_point(config_data)

    def cleanup_credentials_file(self, config_data):
        """Deletes the credentials file."""
        credentials_file = Path(config_data.credentials_filepath)
        if credentials_file.exists():
            try:
                credentials_file.unlink()
                self.text_edit.append("Credentials file deleted.")
            except Exception as e:
                self.text_edit.append(f"Failed to delete credentials file: {e}")

    def remove_fstab_entry(self, config_data):
        """Removes the added entry from /etc/fstab using pyfstab."""
        try:
            fstab = Fstab(path=config_data.fstab_location)
            # Find the entry to remove
            entry_to_remove = None
            for entry in fstab:
                if (
                    entry.fs_spec
                    == f"//{config_data.samba_ip}/{config_data.samba_share}"
                    and entry.fs_file == config_data.samba_path
                ):
                    entry_to_remove = entry
                    break
            if entry_to_remove:
                fstab.remove_entry(entry_to_remove)
                fstab.write()
                self.text_edit.append("Removed the fstab entry.")
                return True
            else:
                self.text_edit.append("Fstab entry not found.")
                return False
        except Exception as e:
            self.text_edit.append(f"Failed to remove fstab entry: {e}")
            return False

    def delete_mount_point(self, config_data):
        """Deletes the mount point if it was created by the program."""
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
