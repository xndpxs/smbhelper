import re


def validate_ip(ip_address):
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return re.match(pattern, ip_address) is not None


def validate_non_empty(value):
    return bool(value and value.strip())
