#
import src
import src.driver
import src.system
#
class Device:
    """ root device of the system
    """
    Items = []
    @staticmethod
    def init():
        """ initialized the system device
        """
        service = src.Service(('localhost', 64001), Device.__servicehandler)
        service.start()
        payload = {'Device': 'Board', 'Methode': 'GetItems'}
        service.transmitter(payload, ('localhost', 64000))
        return Device
    #
    @staticmethod
    def __servicehandler(event: int, *args):
        """ this function called by driver event
        """
        __return = None
        __payload = {}
        if event == src.driver.Board.Events.SYSTEM:
            __payload = args[1]
            __device = __payload['Device']
            #
            if __device == 'Board':
                Device.__board(__payload)
            elif __device == 'Button':
                pass
    #
    @staticmethod
    def __board(payload: {}):
        __methode = payload['Methode']
        if __methode == 'GetItems':
            __count = payload['Count']
            for __item in range(0, __count):
                __type = payload[str(__item)]['Type']
                __name = payload[str(__item)]['Name']
                #
                #pylint: disable-msg=protected-access
                if __type == 'Button':
                    __control = src.system.Button(src.system.Device, __name, src.system.Device.__servicehandler, payload[str(__item)]['Mode'])
                    Device.Items.append(__control)
                elif __type == 'Relay':
                    __control = src.system.Relay(src.system.Device, __name, src.system.Device.__servicehandler)
                    Device.Items.append(__control)
                elif __type == 'Station':
                    __control = src.system.Station(src.system.Device, __name, src.system.Device.__servicehandler)
                    Device.Items.append(__control)
                #pylint: enable-msg=protected-access
        pass
#
class Control:
    """
    base class of control objects

    Keyword arguments:
    parent -- parent of the object
    ident -- ID of the object
    kind -- type of the object
    eventhandler -- handler by event
    """
    def __init__(self, parent: object, ident: str, kind: object, eventhandler):
        self.parent = parent
        self.ident = ident
        self.kind = kind
        self.eventhandler = eventhandler
        self._properties = {}
        self.__active = False
    #
    def properties(self) -> {}:
        """ return the properties of the object
        """
        return self._properties
    #
    def active(self, value=0) -> bool:
        """ set or get active value
        """
        __return = int
        if value == 0:
            __return = self.__active
        else:
            self.__active = value
            __return = None
        return __return
    #
    class Kind:
        """ types of objects
        """
        #
        # types of system objects
        # interfaces
        Station = 11
        AccessPoint = 12
        Ethernet = 13
        Bluetooth = 14
        SDCard = 13
        # sensors
        Button = 20
        Switch = 21
        # parts
        Relay = 30
        Led = 31
        # end types of system objects
    #
#
