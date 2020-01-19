import json
import socket
#
import src
from .board import Board
#
class Simulation(Board):
    """ static class device.simulation.Board
    """
    def __init__(self):
        super().__init__()
        self.service = src.Service(('localhost', 64000), self.__servicehandler)
        self.service.start()
        self.tcp = None
        self.udp = None
        self.ssdp = None
    #
    def __servicehandler(self, event: int, *args):
        __return = None
        __payload = {}
        if event == Board.Events.SYSTEM:
            __payload = args[1]
            __device = __payload['Device']
            #
            if __device == 'Board':
                __return = self.__board(__payload)
                __payload.update(__return)
                __return = __payload
            elif __device == 'Button':
                pass
            elif __device == 'Relay':
                pass
            elif __device == 'Station':
                pass
        if __return != '':
            self.service.transmitter(__return, ('localhost', 64001))
    #
    def __station(self, payload: {}):
        __return = None
        __methode = payload['Methode']
        if __methode == 'Connect':
            __ssid = payload['SSID']
            __pw = payload['Password']
            __mode = payload['Mode']
            if __mode != 'DHCP':
                __ip = payload['IP']
                __mask = payload['SubnetMask']
                __dns = payload['DNS']
    #
    def __board(self, payload: {}):
        __return = None
        __methode = payload['Methode']
        if __methode == 'GetItems':
            __return = {
                "Count" : 4,
                "0" : {
                    "Type" : "Button",
                    "Name" : "Button",
                    "Mode" : "OnHold"
                },
                "1" : {
                    "Type" : "Relay",
                    "Name" : "RelayOne"
                },
                "2" : {
                    "Type" : "Relay",
                    "Name" : "RelayTwo"
                },
                "3" : {
                    "Type" : "Station",
                    "Name" : "Station"
                }
            }
        elif __methode == '':
            pass
        return __return
    #
    class TCP:
        """ service interface between device and system layer
        """
        def __init__(self, address, function):
            """ initialize the device service
            """
            self.handler = function
            self.address = address
            self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #pylint: disable-msg=too-many-function-args
            self.interface.bind(self.address)
            #pylint: enable-msg=too-many-function-args
            self.loop = src.Loop(0.1, self.__receiver)
        #
        def start(self):
            """ started the service
            """
            self.loop.start()
        #
        def stop(self):
            """ stoped the service
            """
            self.loop.stop()
            #pylint: disable-msg=too-many-function-args
            self.interface.close()
            #pylint: enable-msg=too-many-function-args
        #
        def __receiver(self, *args):
            del args
            #pylint: disable-msg=assignment-from-no-return
            #pylint: disable-msg=too-many-function-args
            __data, __con = self.interface.recvfrom(1024)
            __encode = json.loads(__data)
            #pylint: enable-msg=too-many-function-args
            #pylint: enable-msg=assignment-from-no-return
            self.handler(0, __con, __encode)
        #
        def transmitter(self, data, address):
            """ transmitted data to address
            """
            #pylint: disable-msg=assignment-from-no-return
            #pylint: disable-msg=too-many-function-args
            __decode = json.dumps(data).encode('utf-8')
            self.interface.sendto(__decode, address)
            #pylint: enable-msg=too-many-function-args
            #pylint: enable-msg=assignment-from-no-return
    #
#
