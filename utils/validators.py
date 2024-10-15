import ipaddress


def validate_ip(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False


def validate_non_empty(value):
    return bool(value and value.strip())
