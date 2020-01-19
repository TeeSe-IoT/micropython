import core.devices
import core.models
#
class Process:
    def __init__(self, ID: str, Event: core.devices.Events, Index: int, Steps: {}) -> None:
        self.Index = Index
        self.ID = ID
        self.Event = Event
        self.Steps = Steps
    #
    def Run(self) -> None:
        print('Process ', self.ID, self.Event, ' running!')
        __Loop = True
        __Next = None
        __Index = '1'
        while __Loop:
            __Step = self.Steps['Steps'][__Index]
            __KeyWord = __Step['KeyWord']

            if __KeyWord == 'If':
                __Next = Process.If(__Step)
            elif __KeyWord == 'Function':
                __Next = Process.Function(__Step)
            elif __KeyWord == 'Goto':
                __Next = Process.Function(__Step)
            #
            if __Next == 'Stop':
                __Loop = False
            else:
                __Index = __Next
    #
    @staticmethod
    def If(Tree: {}) -> str:
        __Return = None
        __Operand1 = Process.Operand(Tree['Operand1'])
        __Operand2 = Process.Operand(Tree['Operand2'])
        if Process.Operation(Tree['Operation'], __Operand1, __Operand2):
            __Return = Process.Goto(Tree['True'])
        else:
            __Return = Process.Goto(Tree['False'])
        print('If returns:', __Return)
        return __Return
    #
    @staticmethod
    def Operation(Type: str, Left: None, Right: None) -> bool:
        __Return = False
        if Type == 'Equal':
            if Left == Right:
                __Return = True
        elif Type == 'NotEqual':
            if Left != Right:
                __Return = True
        print('Operation returns:', __Return)
        return __Return
    #
    @staticmethod
    def Operand(Tree: {}) -> object:
        __Return = None
        __Object = None
        __KeyWord = Tree['KeyWord']
        if __KeyWord == 'Function':
            __Return = Process.Function(Tree, False)
        elif __KeyWord == 'Value':
            __Return = Process.Value(Tree)
        print('Operand returns:', __Return)
        return __Return
    #
    @staticmethod
    def Function(Tree: {}, Next=True) -> object:
        __Return = None
        __Call = Tree['Call']
        if __Call == 'Device':
            __Type = Tree['Type']
            if __Type == 'Local':
                __Device = core.devices.Board.FindDevice(Tree['ID'])
                if Tree['Method'] == 'GetState':
                    __Return = __Device.GetState()
                elif Tree['Method'] == 'SetState':
                    __Device.SetState(Tree['Value'])
            elif __Type == 'Remote':
                pass
        #
        if Next == 1:
            __Return = Process.Goto(Tree)
        print('Function returns:', __Return)
        return __Return
    #
    @staticmethod
    def Value(Tree: {}) -> object:
        print('Value returns:', Tree['Value'])
        return Tree['Value']
    #
    @staticmethod
    def Goto(Tree: {}) -> str:
        print('Goto returns:', Tree['Line'])
        return Tree['Line']
