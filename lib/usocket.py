"""
Module: 'usocket' on esp32 1.11.0
"""
# MCU: (sysname='esp32', nodename='esp32', release='1.11.0', version='v1.11-132-gc24d81119 on 2019-07-08', machine='ESP32 module with ESP32')
# Stubber: 1.2.0
AF_INET = 2
AF_INET6 = 10
IPPROTO_IP = 0
IPPROTO_TCP = 6
IPPROTO_UDP = 17
IP_ADD_MEMBERSHIP = 3
SOCK_DGRAM = 2
SOCK_RAW = 3
SOCK_STREAM = 1
SOL_SOCKET = 4095
SO_REUSEADDR = 4
def getaddrinfo(host, port, af=0, type=0, proto=0, flags=0):
    pass

def inet_pton(family, txt_address) -> bytes:
    pass


class socket:
    ''
    def accept():
        pass

    def bind(self, address):
        pass

    def close():
        pass

    def connect(self, address):
        pass

    def fileno():
        pass

    def listen(self, maxconnections) -> usocket:
        pass

    def makefile():
        pass

    def read():
        pass

    def readinto():
        pass

    def readline():
        pass

    def recv(self, bufsize) -> [bytes]:
        pass

    def recvfrom(self, bufsize) -> (data, address):
        pass

    def send(self, data):
        pass

    def sendall():
        pass

    def sendto(self, data, address):
        pass

    def setblocking(self, bool):
        pass

    def setsockopt():
        pass

    def settimeout():
        pass

    def write():
        pass

