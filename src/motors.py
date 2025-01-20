# https://docs.circuitpython.org/projects/motorkit/en/latest/index.html
import board
from adafruit_motorkit import MotorKit


# def getMotors(address=0x60):
#     kit = MotorKit(address=0x60, i2c=board.I2C())
#     return (kit.motor1, kit.motor2)

class Motors:
    def __init__(self, address=0x60, i2c=board.I2C()):
        self._kit = MotorKit(address=address, i2c=i2c)
        self.motor1, self.motor2 = (self._kit.motor1, self._kit.motor2)
        self.motor1.throttle = 0.0
        self.motor2.throttle = 0.0
