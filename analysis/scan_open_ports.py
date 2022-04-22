import socket
import logging
import time
import sys
import asyncio

class SocketConnection:
    def __init__(self, ip, port=None):
        self.socket = None
        self.ip = ip    

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        return self

    def __exit__(self, type, value, traceback):
        self.socket.close()
        self.socket = None

    def portscan(self, port):

        if self.socket is None:
            raise ConnectionError('No socket open')
        try:
            res = self.socket.connect_ex((self.ip, port))
            # print(f"{port}: {res}")
            return not res
        finally:
            self.socket.detach()

def scan_ports(ip, port_range):
    """yields the open ports in `port_range` (port_range is half-open) """
    ports = []
    ports_refused = []

    # print("scanned: ")
    for port in range(*port_range):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        res = sock.connect_ex((ip, port))
        if res == 0:
            ports.append(port)
        elif res == 111:
            ports_refused.append(port)
        sock.close()
        # print(f"{port}: {res}")
    
    print(f"open ports: {ports}")
    print(f"open but connection refused: {ports_refused}")
    return ports

def main():
    logging.basicConfig(filename="errlog.log", format="%(asctime)s : %(message)s")
    logging.info("Start")
    message = """
    Hello user and welcome to Network Port Scanner!
    Please insert a IP address that you want to scan for open and closed ports.
    The range of ports scanned is 1-65535.
    """
    print(message)
    # ip = sys.argv[1]
    ip = '3.67.8.147'
    ip = '216.239.38.21'

    scan_ports(ip, (1, 444))

    # open_ports = list(scan_ports(ip, (442, 444)))

    # print(
    #     f"""open ports: ({len(open_ports)})
    #     {open_ports}""")

if __name__ == '__main__':
    main()