import os
import time
from getpass import getpass


# -----------------FOLDER CREATION-----------------------------------
# Create the credentials folder in specified path
def create_credentials_folder(path_credentials):
    if os.path.exists(path_credentials):
        print(" Folder for credentials already found. Using it...")
    else:
        try:
            print(" Folder not found, creating one...")
            os.makedirs(path_credentials, 0o700, exist_ok=True)
            print(" Folder for credentials created...")
        except Exception as error:
            print(f" Can't create credentials folder: {error}")


# ------------------FILE CREDENTIALS CREATION--------------------------
def create_credentials_file(user, passw, domain, credentials_file):
    try:
        print(f"{credentials_file}")
        if os.path.exists(credentials_file):  # File Exists Already
            overwrite = (
                input("File already found, do you want to rewrite it? y/n: ").lower()
                == "y"
            )
            if not overwrite:  # We Shouldn't Overwrite it
                print("New credentials file Not Created...")
                return
        with open(credentials_file, "w", 0o600) as file:  # w already overwrite it.
            file.write(f"username={user}\n")
            file.write(f"password={passw}\n")
            file.write(f"domain={domain}\n")
        print("File created")
    except Exception as error:
        print(f"Can't create file: {error}")


# ---------------------------MODIFYING FSTAB----------------------------------
def fstab_modify(entry):
    try:
        # Read existing entries from fstab
        with open("/etc/fstab", "r") as f:
            lines = f.readlines()

        # Check if the entry already exists
        if any(line.strip() == entry.strip() for line in lines):
            print(
                f"A line in /etc/fstab for {entry} already exists. New entry not added."
            )
        else:
            # Append the new entry to fstab
            with open("/etc/fstab", "a") as f:
                f.write(entry)
                print(f"New entry on /etc/fstab for {entry} added.")

            # # Print the updated contents of fstab
            # print("Updated /etc/fstab:")
            # with open("/etc/fstab", "r") as f:
            #     print(f.read())
    except Exception as e:
        print(f"Error at adding the entry on /etc/fstab: {e}")


# ----------------------SHARE FOLDER CHECK-----------------------------
def check_folder_share(mount_folder):
    try:
        if os.path.exists(mount_folder):
            print("Folder for smb mounting found, using it.")
        else:
            os.makedirs(mount_folder, exist_ok=True)
            os.chown(mount_folder, 1000, 1000)
    except Exception as error:
        print(f"Can't create folder: {error}")


# ---------------------VALIDATING FSTAB------------------------------
def validate_fstab():
    try:
        # Reload daemons
        os.system("systemctl daemon-reload")
        # Mount all entrances in /etc/fstab
        mount_result = os.system("mount -a")
        if mount_result != 0:
            print("Error mounting entries in /etc/fstab.")
            return False
        else:
            print("Entries successfully mounted in /etc/fstab.")
            return True
    except Exception as e:
        print(f"Error validating /etc/fstab: {e}")
        return False


# --------------------------RETURN TO BEGINNING IF ERROR----------------------
def cleanup_func(credentials_file, fstab_entr, fstab_loc):
    if os.path.exists(credentials_file):
        os.remove(credentials_file)
        print("Removed credentials file")

    with open(fstab_loc, "r") as f:
        lines = f.readlines()
    with open(fstab_loc, "w") as f:
        for line in lines:
            if line.strip() == fstab_entr.strip():
                f.write(line)


# ----------------------------MAIN--------------------------------------------
def main():
    ############### Configurable Variables ###################################
    mnt_folder = input("Local folder address:")
    samba_server_ip = input("IP address Samba Server:")
    share_name = input("Share Name: ")
    samba_user = input("Samba username: ")
    samba_pass = getpass("Samba password: ")
    samba_domain = input("Domain(optional): ")
    samba_path_credentials = "/etc/samba/credentials"
    credentials_filename = samba_server_ip + "_credentials"
    fstab_location = "/etc/fstab"
    credentials_filepath = samba_path_credentials + "/" + credentials_filename
    fstab_entry = f"//{samba_server_ip}/{share_name} {mnt_folder} cifs rw,x-systemd.automount,credentials={credentials_filepath},uid=1000,gid=1000 0 0\n"
    ###########################################################################

    print("Creating the folder...")
    time.sleep(1)
    create_credentials_folder(samba_path_credentials)

    print("Creating the credentials file inside '/etc/samba/credentials'...")
    time.sleep(1)
    create_credentials_file(samba_user, samba_pass, samba_domain, credentials_filepath)

    print("Creating mount folder...")
    time.sleep(1)
    check_folder_share(mnt_folder)

    print("Adding fstab entry...")
    time.sleep(1)
    fstab_modify(fstab_entry)

    print("checking fstab entries...")
    time.sleep(1)
    if validate_fstab():
        print(
            "All fstab entries validated and mounted :) Enjoy your new SMB automount!"
        )
    else:
        cleanup_func(credentials_filepath, fstab_entry, fstab_location)


if __name__ == "__main__":
    main()
