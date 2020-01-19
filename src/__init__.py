import json
import socket
import time
import _thread as thread
#
#
def eventnothing(event: int, *args):
    """
    Keyword arguments:
    event -- number of the event
    args -- optional arguments
    """
    del args
    del event
    print('Event Nothing!')
#
class Loop:
    def __init__(self, timespan, function, *functionargs):
        self.__active = False
        self.__function = function
        self.__functionargs = functionargs
        self.__timespan = timespan
        self.__thread = object
    #
    def start(self):
        self.__thread = thread.start_new_thread(self.__worker, ())
        self.__active = True
    #
    def stop(self):
        self.__active = False
    #
    def __worker(self):
        while self.__active:
            self.__function(self.__functionargs)
            time.sleep(self.__timespan)
#
class Service:
    """ service interface between device and system layer
    """
    def __init__(self, address, function):
        """ initialize the device service
        """
        self.handler = function
        self.address = address
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #pylint: disable-msg=too-many-function-args
        self.interface.bind(self.address)
        #pylint: enable-msg=too-many-function-args
        self.loop = Loop(0.1, self.__receiver)
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
