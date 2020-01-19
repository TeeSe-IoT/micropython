import sys
#
import src.system
import src.driver
#
if sys.argv[0] != 'main.py':
    sys.path.insert(0, 'c:/Develope/templates/esp32-micropython-vscode/lib')
#
DRIVER = src.driver.Simulation()
SYSTEM = src.system.Device.init()
# forever
while True:
    pass
