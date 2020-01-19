from .system import Control
#
class Relay(Control):
    """ Relay
    """
    # Constructor
    def __init__(self, parent: object, ident: str, eventhandler) -> None:
        Control.__init__(self, parent, ident, Control.Kind.Relay, eventhandler)
    # Events
    # Properties
    # Methodes
#
