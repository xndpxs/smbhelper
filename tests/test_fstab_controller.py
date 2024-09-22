import pytest
import subprocess
from unittest.mock import patch, MagicMock, mock_open
from controllers.fstab_controller import FstabController
from models.config_data import ConfigData
from pathlib import Path


@pytest.fixture
def setup_fstab_controller():
    """Fixture to set up the FstabController and ConfigData."""
    text_edit = MagicMock()  # Mock QTextEdit widget to capture text output
    controller = FstabController(text_edit)
    config_data = ConfigData(
        samba_ip="192.168.0.1",
        samba_share="testshare",
        samba_user="testuser",
        samba_pass="password",
        samba_domain="",
        samba_path="/mnt/test",
    )

    config_data.fstab_location = "/etc/fstab"
    config_data.credentials_filepath = "/etc/samba/credentials/test_credentials"
    return controller, config_data, text_edit


@patch("controllers.fstab_controller.getpwnam")
def test_prepare_fstab_entry_success(mock_getpwnam, setup_fstab_controller):
    """Test the successful preparation of the fstab entry."""
    controller, config_data, text_edit = setup_fstab_controller
    mock_getpwnam.return_value = MagicMock(pw_uid=1000, pw_gid=1000)
    result = controller.prepare_fstab_entry(config_data)
    assert result is True
    text_edit.append.assert_any_call("Fstab entry prepared successfully.")


@patch("builtins.open", new_callable=mock_open, read_data="existing_entry")
def test_entry_exists_true(mock_file, setup_fstab_controller):
    """Test that the entry exists check returns True when the entry is found."""
    controller, config_data, _ = setup_fstab_controller
    config_data.fstab_entry = "existing_entry"
    result = controller.entry_exists(config_data)
    assert result is True


@patch("builtins.open", new_callable=mock_open, read_data="different_entry")
def test_entry_exists_false(mock_file, setup_fstab_controller):
    """Test that the entry exists check returns False when the entry is not found."""
    controller, config_data, _ = setup_fstab_controller
    config_data.fstab_entry = "missing_entry"
    result = controller.entry_exists(config_data)
    assert result is False


@patch("builtins.open", new_callable=mock_open)
def test_append_entry_success(mock_file, setup_fstab_controller):
    """Test appending a new entry to the fstab file."""
    controller, config_data, _ = setup_fstab_controller
    result = controller.append_entry(config_data)
    assert result is True
    mock_file().write.assert_called_with(config_data.fstab_entry + "\n")


@patch("shutil.copyfile")
def test_create_backup_success(mock_copyfile, setup_fstab_controller):
    """Test that the backup creation of fstab is successful."""
    controller, config_data, _ = setup_fstab_controller
    result = controller.create_backup(config_data)
    assert result is True
    mock_copyfile.assert_called_with(Path("/etc/fstab"), Path("/etc/fstab.bak"))


@patch("subprocess.run")
def test_validate_and_mount_success(mock_subprocess, setup_fstab_controller):
    """Test successful mount validation."""
    controller, config_data, text_edit = setup_fstab_controller
    mock_subprocess.return_value = MagicMock(returncode=0)
    result = controller.validate_and_mount(config_data)
    assert result is True
    # Verificar las llamadas en el orden correcto
    text_edit.append.assert_any_call("Attempting to mount the share...")
    text_edit.append.assert_any_call("Mount successful.")
    text_edit.append.assert_any_call("Unmounted the share after validation.")


@patch("subprocess.run", side_effect=subprocess.CalledProcessError(32, "mount"))
def test_validate_and_mount_fail(mock_subprocess, setup_fstab_controller):
    """Test mount validation failure."""
    controller, config_data, text_edit = setup_fstab_controller
    result = controller.validate_and_mount(config_data)
    assert result is False
    text_edit.append.assert_called_with(
        "Mount failed: Command 'mount' returned non-zero exit status 32."
    )


@patch("builtins.open", new_callable=mock_open, read_data="entry_to_remove\n")
def test_remove_fstab_entry_success(mock_file, setup_fstab_controller):
    """Test successful removal of the fstab entry."""
    controller, config_data, text_edit = setup_fstab_controller
    config_data.fstab_entry = "entry_to_remove"
    result = controller.remove_fstab_entry(config_data)
    assert result is True
    text_edit.append.assert_called_with("Removed the fstab entry.")


@patch("pathlib.Path.rmdir")
def test_delete_mount_point_success(mock_rmdir, setup_fstab_controller):
    """Test successful deletion of the mount point."""
    controller, config_data, text_edit = setup_fstab_controller
    config_data.mount_point_created = True
    result = controller.delete_mount_point(config_data)
    assert result is True
    mock_rmdir.assert_called_once()
    text_edit.append.assert_called_with(
        f"Deleted mount point at {config_data.samba_path}."
    )
