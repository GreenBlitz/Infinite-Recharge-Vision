import platform
import socket


def is_on_rpi() -> bool:
    return platform.uname()[4].startswith('arm')


def is_on_roborio_network() -> bool:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip.startswith('10.45.90.')
