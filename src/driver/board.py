class Board:
    """ parent class for specific board driver
    """
    def __init__(self) -> None:
        pass
    #
    def __servicehandler(self) -> None:
        pass
    #
    class Events:
        """ enum of events driver layer
        """
        SYSTEM = 0
        DRIVER_REQUEST = 10
        DRIVER_RESPONSE = 11
        DRIVER_EVENT = 12
#
