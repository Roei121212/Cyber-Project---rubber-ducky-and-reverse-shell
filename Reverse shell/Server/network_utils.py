import socket
import constants


def find_local_ipv4addr():
    return constants.IP


def recv_all(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(min(size - len(data), 4096))
        if not chunk:
            break
        data += chunk
    return data
