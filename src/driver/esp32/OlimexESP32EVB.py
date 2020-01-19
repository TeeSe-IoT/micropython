import gc
import socket
import time
import stubs.network as network
import stubs.machine as machine
import _thread as thread
#
import core.devices
import core.devices.interfaces
import core.devices.parts
import core.devices.sensors
import core.models
#
SSID = 'UnserWLAN#1'
Password = '$wlan8a0e#Am'
#
class System:
    __Thread_Exit = False
    __Button_Pin = machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_UP)
    __Relay0_Pin = machine.Pin(32, machine.Pin.OUT)
    __Relay1_Pin = machine.Pin(33, machine.Pin.OUT)
    __Station_Interface = network.WLAN(network.STA_IF)
    __Station_UDPReceiver_Thread = None
    __Station_UDPReceiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    __DefaultProcessSteps = {
        'Steps': {
            '1': {
                'KeyWord': 'If',
                'Operand1': {
                    'KeyWord': 'Function',
                    'Call': 'Device',
                    'Type' : 'Local',
                    'ID': 'UUID-01',
                    'Method': 'GetState'
                },
                'Operation': 'Equal',
                'Operand2': {
                    'KeyWord': 'Value',
                    'Value': 0
                },
                'True': {
                    'Line':'2'
                },
                'False': {
                    'Line':'4'
                }
            },
            '2': {
                'KeyWord': 'Function',
                'Call': 'Device',
                'Type' : 'Local',
                'ID': 'UUID-01',
                'Method': 'SetState',
                'Value': 1,
                'Line': '3'
            },
            '3': {
                'KeyWord': 'Function',
                'Call': 'Device',
                'Type' : 'Local',
                'ID': 'UUID-02',
                'Method': 'SetState',
                'Value': 1,
                'Line': 'Stop'
            },
            '4': {
                'KeyWord': 'Function',
                'Call': 'Device',
                'Type' : 'Local',
                'ID': 'UUID-01',
                'Method': 'SetState',
                'Value': 0,
                'Line': '5'
            },
            '5': {
                'KeyWord': 'Function',
                'Call': 'Device',
                'Type' : 'Local',
                'ID': 'UUID-02',
                'Method': 'SetState',
                'Value': 0,
                'Line': 'Stop'
            }
        }
    }
    #
    @staticmethod
    def Init():
        # Init Parameters
        core.devices.Board.ID = 'UUID'
        core.devices.Board.Name = 'Olimex ESP32-EVB'
        core.devices.Board.SOCType = core.devices.SOCTypes.ESP32
        core.devices.Board.Reset = System.__Board_Reset()
        # Init Processing
        __Process = core.models.Process(core.devices.Board.ID + '-00', core.devices.Events.Button_Pushed, len(core.devices.Board.Processes), System.__DefaultProcessSteps)
        core.devices.Board.Processes.append(__Process)
        # Init Devices
        # Button
        __Button = core.devices.sensors.Button(core.devices.Board.ID + '-00', len(core.devices.Board.Devices), core.devices.Board, System.__Button_GetMode, System.__Button_GetState)
        __Button_Pin_CallBack = System.__Button_Pin.irq(__Button.EventPushed, machine.Pin.IRQ_FALLING)
        __Button.OnPushed = core.devices.Board.Handler
        core.devices.Board.Devices.append(__Button)
        # Relay0
        __Relay0 = core.devices.parts.Relay(core.devices.Board.ID + '-01', len(core.devices.Board.Devices), core.devices.Board, System.__Relay0_GetState, System.__Relay0_SetState)
        core.devices.Board.Devices.append(__Relay0)
        # Relay1
        __Relay1 = core.devices.parts.Relay(core.devices.Board.ID + '-02', len(core.devices.Board.Devices), core.devices.Board, System.__Relay1_GetState, System.__Relay1_SetState)
        core.devices.Board.Devices.append(__Relay1)
        # Global
        gc.collect()
        System.__Thread_Exit = False
        # Station
        System.__Station_Interface.active(True)
        System.__Station_Interface.connect(SSID, Password)
        time.sleep(1)
        System.__Station_UDPReceiver.bind((System.__Station_Interface.ifconfig()[1], 1965))
        System.__Station = core.devices.interfaces.Station(core.devices.Board.ID + '-03', len(core.devices.Board.Devices), core.devices.Board, None, None, None)
        # System.__Station_UDPThread = thread.start_new_thread(System.__Station_UDPReceiver_Task(), ())
        #
        print('class OlimexESP32EVB is initialized')
    #
    @staticmethod
    def __Station_Event():
        pass
    #
    @staticmethod
    def __Station_UDPReceiver_Task():
        while True:
            __ReceivedData, __SendingAddr = System.__Station_UDPReceiver.recvfrom(1024)
            System.__Station.Event(__ReceivedData, __SendingAddr)
            if System.__Thread_Exit == 1:
                System.__Station_UDPReceiver.close()
                thread.exit()
    #
    @staticmethod
    def __Board_Reset():
        # machine.soft_reset()
        pass
    #
    @staticmethod
    def __Button_GetMode():
        return core.devices.sensors.Button.ButtonMode.Falling
    #
    @staticmethod
    def __Button_GetState():
        _Return = System.__Button_Pin.value()
        if _Return == 0:
            _Return = core.devices.sensors.Button.ButtonState.Up
        else:
            _Return = core.devices.sensors.Button.ButtonState.Down
        return _Return
    #
    @staticmethod
    def __Relay0_GetState():
        return System.__Relay0_Pin.value()
    #
    @staticmethod
    def __Relay1_GetState():
        return System.__Relay0_Pin.value()
    #
    @staticmethod
    def __Relay0_SetState(Value):
        System.__Relay0_Pin.value(Value)
    #
    @staticmethod
    def __Relay1_SetState(Value):
        System.__Relay1_Pin.value(Value)
