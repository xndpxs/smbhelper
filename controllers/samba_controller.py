from pathlib import Path
import os


class SambaController:
    """Controller class that handles Samba configuration operations."""

    def __init__(self, text_edit):
        """
        Initializes the SambaController.

        :param text_edit: Reference to the QTextEdit widget for displaying messages to the user.
        """
        self.text_edit = text_edit

    def setup_samba(self, config_data, overwrite_credentials=False):
        """
        Sets up Samba by creating the credentials folder and file.

        :param config_data: Instance of ConfigData containing configuration data.
        :param overwrite_credentials: Boolean indicating whether to overwrite existing credentials file.
        """
        self.create_credentials_folder(config_data)
        self.create_credentials_file(config_data, overwrite_credentials)

    def create_credentials_folder(self, config_data):
        """
        Creates the credentials folder if it does not exist.

        :param config_data: Instance of ConfigData containing configuration data.
        """
        credentials_path = Path(config_data.samba_path_credentials)
        if credentials_path.exists():
            self.text_edit.append("Credentials folder already exists.")
        else:
            try:
                credentials_path.mkdir(mode=0o700, parents=True, exist_ok=True)
                self.text_edit.append("Credentials folder created.")
            except PermissionError:
                self.text_edit.append(
                    "Permission denied: Cannot create credentials folder. Please run the program as root."
                )
            except Exception as e:
                self.text_edit.append(f"Error creating credentials folder: {e}")

    def create_credentials_file(self, config_data, overwrite=False):
        """
        Creates the credentials file.

        :param config_data: Instance of ConfigData containing configuration data.
        :param overwrite: Boolean indicating whether to overwrite existing credentials file.
        """
        credentials_file = Path(config_data.credentials_filepath)
        if credentials_file.exists() and not overwrite:
            self.text_edit.append(
                "Credentials file already exists and will not be overwritten."
            )
        else:
            self.write_credentials_file(credentials_file, config_data)

    def write_credentials_file(self, credentials_file, config_data):
        """
        Writes the credentials file with the provided configuration data.

        :param credentials_file: Path to the credentials file.
        :param config_data: Instance of ConfigData containing configuration data.
        """
        try:
            with open(credentials_file, "w") as file:
                file.write(f"username={config_data.samba_user}\n")
                file.write(f"password={config_data.samba_pass}\n")
                file.write(f"domain={config_data.samba_domain}\n")
            os.chmod(credentials_file, 0o600)
            self.text_edit.append("Credentials file written.")
        except PermissionError:
            self.text_edit.append(
                "Permission denied: Cannot write credentials file. Please run the program as root."
            )
        except Exception as e:
            self.text_edit.append(f"Error writing credentials file: {e}")
