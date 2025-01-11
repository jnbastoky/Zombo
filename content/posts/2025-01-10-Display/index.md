+++
title = 'The Display'
date = 2025-01-10
draft = false
categories = ["update"]
tags = ["zombo", "display"]
thumbnail = "display.png"
+++

We are starting with the display. I think this will be useful since it can
provide some feedback without having to use the serial terminal.

## Summary

We plan on showing the following information on the display:

- Current State/Action
- Current Command
- Diagnostic Information

## Hardware

We are using the [Adafruit OLED Feather Wing][feather-wing-oled].  It's white a
black and while 128x64 OLED display.  It communicates with the microcontroller
via I2C.  There are 3 buttons on board the Feather Wing that we might use for
something later.

[![OLED Feather Wing Display](display.png "OLED Feather Wing Display")](display.png)

## Software

This display is supported by the Adafruit Circuit Python
`adafruit_displayio_sh1107` library.  So we can easily write text to the
display.

We are creating our own `Display` wrapper class to keep the main `code.py` cleaner.

```python
import board
import board
import displayio
from adafruit_display_text import bitmap_label
import adafruit_displayio_sh1107
from i2cdisplaybus import I2CDisplayBus
import terminalio

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64

displayio.release_displays()


class Display:
    def __init__(self, address=0x3C, i2c=board.I2C()):
        self._display_bus = I2CDisplayBus(i2c, device_address=address)

        self._display = adafruit_displayio_sh1107.SH1107(
            self._display_bus,
            width=WIDTH,
            height=HEIGHT
        )

        # Make the display context
        self._group = displayio.Group()
        self._display.root_group = self._group
```

We wil keep it simple for now and just include one method to add text to the
display.  The `add_text()` method returns a reference to the text that was
added so that it can be modified later if desired.

```python
    def add_text(self, text, x, y, color=0xFFFFFFFF, scale=1):
        # Draw some label text
        text_area = bitmap_label.Label(terminalio.FONT,
                                       text=text,
                                       color=color,
                                       x=x,
                                       y=y,
                                       scale=scale)
        self._group.append(text_area)
        return text_area

```

The display can also be put to sleep for energy savings.  So we can expose that
functionaly as well in the class.  It might come in handy later.

```python
    def sleep(self):
        print('Display is sleeping.')
        self._display.sleep()

    def wake(self):
        print('Display is waking.')
        self._display.wake()

    def is_awake(self):
        return self._display.is_awake
```

The display _Feather Wing_ has 3 "bonus" buttons on the board
labelled __A__, __B__, and __C__.  I created `Button` class to simplify setup
of the button input pins.  You just pass it the pin and it configures the
input.

```python
from digitalio import DigitalInOut, Direction, Pull


class Button:
    def __init__(self, pin, pullup=True):
        self._pin = DigitalInOut(pin)
        self._pin.direction = Direction.INPUT
        if pullup:
            self._pin.pull = Pull.UP

    def value(self):
        return not self._pin.value
```

I ended up adding `Button` attributes `A`, `B`, and `C` to the `Display` class.
So now the buttons get configured along with the display and are already
clearly associated with the display.

```python {linenos=table,hl_lines=[1, "4-9", "14-16", 31]}
from button import Button

class Display:
    class Buttons:
        '''This class encapsulates the 3 on-board buttons.'''
        def __init__(self, pin_A, pin_B, pin_C):
            self.A = Button(pin_A)
            self.B = Button(pin_B)
            self.C = Button(pin_C)

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

```

## In Action

{{< instagram DEYnMpnMw0e >}}

[feather-wing-oled]: https://www.adafruit.com/product/4650
