# views/smb_view.py

from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox
from PySide6.QtCore import Qt
from .ui.ui_smbwindow import Ui_SMBWindow
from models.config_data import ConfigData
from controllers.samba_controller import SambaController
from controllers.fstab_controller import FstabController
from utils.validators import validate_ip, validate_non_empty
from pathlib import Path


class SmbView(QMainWindow, Ui_SMBWindow):
    """Class that handles the graphical user interface."""

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.config_data = ConfigData()
        self.samba_controller = SambaController(self.text_edit)
        self.fstab_controller = FstabController(self.text_edit)

        # Connect signals and slots
        self.button_apply.clicked.connect(self.apply_clicked)
        self.button_cancel.clicked.connect(self.close_clicked)
        self.actionQuit.triggered.connect(self.close_clicked)
        self.button_search.clicked.connect(self.folder_search)

    def close_clicked(self):
        """Handles the close button click event."""
        self.app.quit()

    def apply_clicked(self):
        """Handles the apply button click event."""
        self.disable_apply_button()
        self.text_edit.append("Processing input...")
        QApplication.processEvents()

        if not self.collect_config_data():
            self.text_edit.append("Failed to get configuration data.")
            self.enable_apply_button()
            return

        if not self.validate_inputs():
            self.text_edit.append("Configuration aborted due to invalid input.")
            self.enable_apply_button()
            return

        if not self.prepare_fstab_entry():
            self.text_edit.append("Failed to prepare fstab entry.")
            self.enable_apply_button()
            return

        if not self.setup_samba():
            self.text_edit.append("Failed to set up Samba credentials.")
            self.enable_apply_button()
            return

        if not self.create_mount_point():
            self.text_edit.append("Failed to create mount point.")
            self.enable_apply_button()
            return

        if not self.modify_fstab():
            self.text_edit.append("Failed to modify /etc/fstab.")
            self.enable_apply_button()
            return

        if self.validate_and_mount():
            self.text_edit.append("Configuration completed successfully.")
        else:
            self.text_edit.append("Mount validation failed.")
            self.handle_failure()
            self.text_edit.append("Changes have been rolled back.")

        self.enable_apply_button()

    def disable_apply_button(self):
        """Disables the apply button to prevent multiple clicks."""
        self.button_apply.setEnabled(False)

    def enable_apply_button(self):
        """Enables the apply button."""
        self.button_apply.setEnabled(True)

    def collect_config_data(self):
        """Retrieves configuration data from input fields."""
        # Get data from input fields
        self.config_data.samba_ip = self.line_samba_ip.text()
        self.config_data.samba_share = self.line_samba_share.text()
        self.config_data.samba_user = self.line_samba_user.text()
        self.config_data.samba_pass = self.line_samba_pass.text()
        self.config_data.samba_domain = self.line_samba_domain.text()
        self.config_data.samba_path = self.line_local_folder.text()

        # Update dependent variables
        self.config_data.credentials_filename = (
            f"{self.config_data.samba_ip}_credentials"
        )
        self.config_data.credentials_filepath = f"{self.config_data.samba_path_credentials}/{self.config_data.credentials_filename}"
        return True

    def validate_inputs(self):
        """Validates the user inputs."""
        valid = True
        error_messages = []

        # Validate IP address
        if not validate_ip(self.config_data.samba_ip):
            error_messages.append("Invalid IP address format.")
            valid = False

        # Validate non-empty fields
        if not validate_non_empty(self.config_data.samba_share):
            error_messages.append("Samba share name cannot be empty.")
            valid = False
        if not validate_non_empty(self.config_data.samba_user):
            error_messages.append("Samba username cannot be empty.")
            valid = False
        if not validate_non_empty(self.config_data.samba_pass):
            error_messages.append("Samba password cannot be empty.")
            valid = False
        if not validate_non_empty(self.config_data.samba_path):
            error_messages.append("Local folder path cannot be empty.")
            valid = False

        # Validate local path
        if not self.validate_local_path():
            error_messages.append("Invalid local folder path.")
            valid = False

        # Display error messages
        if error_messages:
            self.text_edit.append("\n".join(error_messages))

        return valid

    def validate_local_path(self):
        """Validates the local folder path."""
        # Check if the path is not empty and is valid
        path = self.config_data.samba_path
        if not path:
            return False
        # Additional validation can be added here
        return True

    def prepare_fstab_entry(self):
        """Prepares the fstab entry using the controller."""
        result = self.fstab_controller.prepare_fstab_entry(self.config_data)
        return result

    def setup_samba(self):
        """Sets up Samba credentials using the controller."""
        credentials_file = Path(self.config_data.credentials_filepath)
        overwrite_credentials = False
        if credentials_file.exists():
            reply = QMessageBox.warning(
                self,
                "Overwrite Credentials File",
                "Credentials file already exists. Do you want to overwrite it?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            overwrite_credentials = reply == QMessageBox.Yes

        self.samba_controller.setup_samba(self.config_data, overwrite_credentials)
        # Assume setup_samba handles errors internally and returns True
        return True

    def create_mount_point(self):
        """Creates the mount point using the controller."""
        result = self.fstab_controller.create_mount_point(self.config_data)
        return result

    def modify_fstab(self):
        """Modifies the /etc/fstab file using the controller."""
        result = self.fstab_controller.modify_fstab(self.config_data)
        return result

    def validate_and_mount(self):
        """Validates the mount using the controller."""
        result = self.fstab_controller.validate_and_mount(self.config_data)
        return result

    def handle_failure(self):
        """Handles the cleanup process in case of failure."""
        self.fstab_controller.cleanup_changes(self.config_data)

    def folder_search(self):
        """Opens a dialog to select a local folder."""
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if selected_dir:
            self.config_data.samba_path = selected_dir
            self.line_local_folder.setText(selected_dir)

    def closeEvent(self, event):
        """Event that is called when the window is closed."""
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
            self.app.quit()
        else:
            event.ignore()
