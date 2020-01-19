from .system import Control
#
class Station(Control):
    """ Station
    """
    # Constructor
    def __init__(self, parent: object, ident: str, eventhandler) -> None:
        Control.__init__(self, parent, ident, Control.Kind.Station, eventhandler)
    # Events
    # Properties
    # Methodes
#
