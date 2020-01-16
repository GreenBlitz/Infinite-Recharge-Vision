import platform
import socket


def is_on_rpi() -> bool:
    return platform.uname()[4].startswith('arm')


def is_on_roborio_network() -> bool:
    return socket.gethostbyname(socket.gethostname()).startswith('10.45.90.')
