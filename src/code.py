import asyncio

import board
import busio

from distance import Distance
from display import Display
from motors import Motors
from voice import Voice


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

voice = Voice(address=0x64, i2c=i2c_main)

motors = Motors(address=0x61, i2c=i2c_main)
left_motor = motors.motor1
right_motor = motors.motor2


async def display_task(display):
    while True:
        # Update Status and Diagnostics
        label_status.text = ('status: '
                             "I'm awake" if display.is_awake() else "I'm asleep")
        await asyncio.sleep(0)


def display_toggle(event):
    if event.released:
        if display.is_awake():
            display.sleep()
        elif not display.is_awake():
            display.wake()


async def main():
    await asyncio.gather(
        display_task(display),
        display.buttons.task(),
        voice.task(),
    )


display.buttons.set_callback("C", display_toggle)

asyncio.run(main())
