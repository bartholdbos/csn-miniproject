from pad4pi import rpi_gpio

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_4_by_4_keypad()
submit_callback = None
pin = ""


def handle_key(key):
    global pin

    if type(key) is int:
        pin += str(key)

    if key == "*":
        pin = ""
        return

    if len(pin) == 4:
        submit_callback(pin)
        pin = ""
        return


def register(submit):
    global submit_callback

    submit_callback = submit

    keypad.registerKeyPressHandler(handle_key)


def cleanup():
    keypad.cleanup()
