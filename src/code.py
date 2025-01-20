import asyncio
from time import sleep

import board
import busio

from distance import Distance
from display import Display
from motors import Motors
from voice import Voice


sleep(5)

# Configure I/O & Buses
i2c_main = board.I2C()
i2c_dist = busio.I2C(scl=board.D11, sda=board.D10, frequency=100000)

# Setup Display
display = Display(i2c=i2c_main)
display.add_text("I'm Zombo!", x=10, y=10, scale=2)
label_status = display.add_text('<status>', x=0, y=32)
label_cmd = display.add_text('<cmd>', x=0, y=50)
label_dist = display.add_text('<dist>', x=20, y=50)


# Sonar Distance Sensor
dist_front = Distance(0x57, i2c_dist)

voice = Voice(address=0x64, i2c=i2c_main)

motors = Motors(address=0x61, i2c=i2c_main)
left_motor = motors.motor1
right_motor = motors.motor2
STARTING_SPEED = 0.5


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


def motors_toggle(event):
    if event.released:
        if left_motor.throttle > 0:
            left_motor.throttle = 0.0
        else:
            left_motor.throttle = STARTING_SPEED
        if right_motor.throttle > 0:
            right_motor.throttle = 0.0
        else:
            right_motor.throttle = STARTING_SPEED


def display_voice_cmd(command):
    label_cmd.text = str(command)


def display_distance(value):
    label_dist.text = f'dist: {value} mm'


async def avoid_collision():
    print('avoiding collision')
    throttle_mem = (left_motor.throttle, right_motor.throttle)
    left_motor.throttle = 0.0
    right_motor.throttle = 0.0
    await asyncio.sleep(0.5)
    left_motor.throttle = -0.5
    right_motor.throttle = -0.25
    await asyncio.sleep(0.5)
    left_motor.throttle, right_motor.throttle = throttle_mem


async def motors_distance(value):
    print('motors dist')
    if value < 50.0:
        print('need to avoid collision')
        await avoid_collision()                    


async def main():
    await asyncio.gather(
        display_task(display),
        display.buttons.task(),
        voice.task(),
        dist_front.task(),
    )


display.buttons.set_callback("C", display_toggle)
display.buttons.set_callback("A", motors_toggle)
# voice.set_cmd_callback(display_voice_cmd)
voice.set_all_callback(display_voice_cmd)
dist_front.set_callback(display_distance)
dist_front.set_callback(motors_distance, is_async=True)

asyncio.run(main())
