+++
title = 'Architecture'
date = 2025-01-03T18:05:05Z
draft = false
categories = ["update"]
tags = ["zombo", "architecture"]
thumbnail = ""
+++

Zombo runs on an [Adafruit ESP32-S3 Feather][adafruit-feather].  We chose this because
it is a powerful microcontroller with WI-FI and Bluetooth radios so that we have
some flexibility for control and communications later.  It supports several serial
protocols and has a flexible GPIO system, but it will primarily communicate with
most peripherals over an I2C bus. This is a widely used protocol and simplifies
the interface to the peripherals.

## Platform

Adafruit has a development/hobby plaform called _Feather_ that makes connecting
microcontrollers to peripherals very simple. We are using an ESP32-S3 _Feather_
and several _Feather Wings_ (peripheral boards).  Adafruit provides libraries for
interfacing these peripherals which makes it very quick to get things up and running.

We will be using _Circuit Python_ for programming the controllers.  This is a port
of _Python_ that was developed for microcontrollers.

## Sub-Systems

We've identified the following sub-systems that we will implement:

1. __Display__ - Provides command feedback and status
2. __Command__ - Uses voice recognition to accept command inputs.
3. __Navigation__ - Uses ultra-sonic distance sensor for collision avoidance.
4. __Motors__ - Two drive wheels and one caster provide locomotion.
5. __Command__ - Uses voice recognition to accept command inputs.
6. __LED__ - It's not a robot without LEDs.  We wil use the addressable NeoPixels.
7. __Diagnostics__ - Monitor Robot health including battery monitor and wireless
signal strength
8. __Power__ - Power will be supplied with a battery.  There are several voltage
requirements.  The microcontroller _Feather_ and the _Feather Wings_ runs on
3.3 VDC,The motors run on 4-6 VDC, and the LEDs use 5 VDC.

We will detail these systems in future post.

## Diagram

{{< generic-figure caption="Architecture" >}}
{{< mermaid >}}
flowchart
    MCU(Microcontroller)
    I2C_Main((Main
    I²C Bus))
    I2C_Dist((Distance
    I²C Bus))

    MCU <---> I2C_Dist
            I2C_Dist <---> Sonar

    MCU <---> I2C_Main
              I2C_Main <--> Display
              I2C_Main <---> Motor[Motor Controller]
              I2C_Main <--> NeoPixel[NeoPixel Driver]
              I2C_Main <---> Voice[Voice Recognition]
              I2C_Main <--> Battery[Battery Monitor]
{{< /mermaid >}}
{{< /generic-figure >}}

[adafruit-feather]: https://www.adafruit.com/product/5323
