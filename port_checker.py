import socket

def check_port(port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    result = sock.connect_ex(("127.0.0.1", port))

    sock.close()

    if result == 0:
        return "OPEN"

    return "CLOSED"

def check_ports(ports):

    results = {}

    for port in ports:
        results[port] = check_port(port)

    return results