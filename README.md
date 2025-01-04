# Zombo
Zombo the Robot

## Microcontroller

Zombo runs on an Adafruit ESP32-S3 Feather.  We chose this because it is a powerful microcontroller with WI-FI and Bluetooth radios so that we have some flexibility for features and communications later.  It supports several serial protocols and has a flexible GPIO system, but it will primarily communicate with most peripherals over an I2C bus.  This is a widely used protocol and simplifies the interface to the peripherals.

## Sub-Systems

Zombo is composed of the following subsystems.

1. __Display__ - Provides command feedback and status
2. __Command__ - Uses voice recognition to accept command inputs.
3. __Navigation__ - Uses ultra-sonic distance sensor for collision avoidance.
4. __Motors__ - Two drive wheels and one caster provide locomotion.
5. __Command__ - Uses voice recognition to accept command inputs.
6. __LED__ - It's not a robot without LEDs.  We wil use the addressable NeoPixels.
7. __Diagnostics__ - Monitor Robot health including battery monitor and wireless signal strength
8. __Power__ - Power will be supplied with a battery.  There are several voltage requirements.  The microcontroller _Feather_ and the _Feather Wings_ runs on 3.3 VDC, The motors run on 4-6 VDC, and the LEDs use 5 VDC.

## I2C Buses

__Bold__ addresses are non-default.

Since the ultrasonic sensor doesn't play nice on the I2C bus[^ultrasonic-i2c] it
will get it's own dedicated bus.

| Device                                   | Bus      | Address   | Available Range   | Sub-system  |
|:---------------------------------------- |:-------- |:---------:|:----------------- | ----------- |
| OLED Display FeatherWing                 | Main     | 0x3C      | 0x3C-0x3D         | Display     |
| DC Motor + Stepper FeatherWing           | Main     | __0x61__  | 0x60-0x7F         | Motors      |
| NeoDriver                                | Main     | 0x60      | 0x60-0x67         | LED         |
| Voice Recognition                        | Main     | 0x64      | Fixed             | Command     |
| Ultrasonic Distance Sensor               | Distance | 0x57      | Fixed             | Navigation  |
| Feather ESP32-S3 onboard batter moniotor | Main     | 0x36      | Fixed             | Diagnostics |

## Development Setup

Setup Python virtual environment

```bash
python -m venv venv
. venv/bin/activate
```

Install Python modules

```bash
pip install -r requirements.txt
```

Install CircuitPython modules

```bash
circup install -r circuitpython-requirements.txt
```

_Note:_ `circup` downloads and stores copies of the packages in `~/.local/share/circup/` or whatever the output of `python -m site --user-base` returns.

## Serial Console

```bash
screen /dev/ttyACM0 115200
```

[^ultrasonic-i2c]:
    > We noticed that while this sensor does work with I2C it's not very 'friendly' - it doesn't like to share the I2C bus, we think it gets confused by other commands and can lock up the bus.
    >
    >-[Adafruit RCWL-1601 Product Description](https://www.adafruit.com/product/4742#tab-description-content)
