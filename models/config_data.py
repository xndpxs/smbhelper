import os


class ConfigData:
    """Class that saves data configuration."""

    def __init__(
        self,
        samba_ip="",
        samba_share="",
        samba_user="",
        samba_pass="",
        samba_domain="",
        samba_path="",
    ):
        self.samba_ip = samba_ip
        self.samba_share = samba_share
        self.samba_user = samba_user
        self.samba_pass = samba_pass
        self.samba_domain = samba_domain
        self.samba_path = samba_path
        # Variables dependientes
        self.samba_path_credentials = "/etc/samba/credentials"
        self.credentials_filename = f"{self.samba_ip}_credentials"
        self.credentials_filepath = os.path.join(
            self.samba_path_credentials, self.credentials_filename
        )
        self.fstab_location = "/etc/fstab"
        self.fstab_entry = ""
        self.uid = None
        self.gid = None
        self.mount_point_created = False
