import os
import netaddr
from typing import Optional


def check_ip_subnet_is_valid(ip: str, subnet_mask: int) -> Optional[str]:
    try:
        netaddr.IPNetwork(f"{ip}/{subnet_mask}")
    except netaddr.AddrFormatError:
        return "Invalid ip format."
    except Exception:
        return "Unknown error."


def ping(ip_addr: str) -> bool:
    response = os.system(f"ping -c 1 {ip_addr}")
    if response == 0:
        return True

    return False
