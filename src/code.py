import board
from display import Display
from button import Button

# Configure I/O & Buses
i2c_main = board.I2C()

# Setup Display
display = Display(i2c=i2c_main)
display.add_text("I'm Zombo!", x=10, y=10, scale=2)
label_status = display.add_text('<status>', x=0, y=32)
label_cmd = display.add_text('<cmd>', x=0, y=50)

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
                         "I'm awake" if display.is_awake() else "I'm asleep")
    label_cmd.text = (
        'ABC Buttons: '
        + ('1' if display.buttons.A.value() else '0')
        + ('1' if display.buttons.B.value() else '0')
        + ('1' if display.buttons.C.value() else '0')
    )
