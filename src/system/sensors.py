from .system import Control
#
class Button(Control):
    """ Button
    """
    # Constructor
    def __init__(self, parent: object, ident: str, eventhandler, mode: str) -> None:
        Control.__init__(self, parent, ident, Control.Kind.Button, eventhandler)
        self.mode = mode
    # Events
    # Properties
    # Methodes
#
