import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice

from display import Display
from distance import Distance

# Configure I/O & Buses
i2c_main = board.I2C()
i2c_dist = busio.I2C(scl=board.D11, sda=board.D10, frequency=100000)

# Setup Display
display = Display(i2c=i2c_main)
display.add_text("I'm Zombo!", x=10, y=10, scale=2)
label_status = display.add_text('<status>', x=0, y=32)
label_cmd = display.add_text('<cmd>', x=0, y=50)

# Sonar Distance Sensor
dist_front = Distance(0x57, i2c_dist)

while True:
    # Get Command Inputs
    pass

    # Evaluation buttons on Display Feather
    if display.buttons.A.value():
        if not display.is_awake():
            display.wake()

    if display.buttons.B.value():
        pass

    if display.buttons.C.value():
        if display.is_awake():
            display.sleep()

    # Update Status and Diagnostics
    label_status.text = ('status: '
                         f'dist {dist_front.read()}')
    label_cmd.text = (
        'ABC Buttons: '
        + ('1' if display.buttons.A.value() else '0')
        + ('1' if display.buttons.B.value() else '0')
        + ('1' if display.buttons.C.value() else '0')
    )
