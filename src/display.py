import board
import displayio
import asyncio

from adafruit_display_text import bitmap_label
import adafruit_displayio_sh1107
from i2cdisplaybus import I2CDisplayBus
import terminalio
from keypad import Keys

from button import Button

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64

displayio.release_displays()


class Display:
    class Buttons:
        '''This class encapsulates the 3 on-board buttons.'''
        def __init__(self, pin_A, pin_B, pin_C, callback_A=None, callback_B=None, callback_C=None):
            self.pin_A = pin_A
            self.callback_A = callback_A
            self.pin_B = pin_B
            self.callback_B = callback_B
            self.pin_C = pin_C
            self.callback_C = callback_C

        def set_callback(self, button, callback):
            if button == 'A':
                self.callback_A = callback
            elif button == 'B':
                self.callback_B = callback
            elif button == 'C':
                self.callback_C = callback
            else:
                raise ValueError(f'button "{button}" not recognized')

        async def task(self):
            pins = (self.pin_A, self.pin_B, self.pin_C)
            callbacks = (self.callback_A, self.callback_B, self.callback_C)
            buttons = Keys(pins, value_when_pressed=False)
            while True:
                event = buttons.events.get()
                if event:
                    # print(event)
                    callback = callbacks[event.key_number]
                    if callback:
                        callback(event)
                # Let another task run.
                await asyncio.sleep(0)

    def __init__(self,
                 address=0x3C,
                 i2c=board.I2C(),
                 pin_A=board.D9,
                 pin_B=board.D6,
                 pin_C=board.D5
                 ):
        self._display_bus = I2CDisplayBus(i2c, device_address=address)

        self._display = adafruit_displayio_sh1107.SH1107(
            self._display_bus,
            width=WIDTH,
            height=HEIGHT
        )

        # Make the display context
        self._group = displayio.Group()
        self._display.root_group = self._group

        # Create buttons
        self.buttons = self.Buttons(pin_A, pin_B, pin_C)

    def add_text(self, text, x, y, color=0xFFFFFF, scale=1):
        text_area = bitmap_label.Label(terminalio.FONT,
                                       text=text,
                                       color=color,
                                       x=x,
                                       y=y,
                                       scale=scale)
        self._group.append(text_area)
        return text_area

    def sleep(self):
        print('Display is sleeping.')
        self._display.sleep()

    def wake(self):
        print('Display is waking.')
        self._display.wake()

    def is_awake(self):
        return self._display.is_awake
