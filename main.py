import keypad
import server
import rfid
import RPi.GPIO as GPIO

alarm_light = 21
alarm = False


def toggle_alarm(cause):
    global alarm

    alarm = not alarm

    if alarm:
        print("Alarm activated by " + cause)
        GPIO.output(alarm_light, 1)

    else:
        print("Alarm deactivated by " + cause)
        GPIO.output(alarm_light, 0)


def trigger_alarm(cause):
    if alarm:
        print("Alarm triggered by" + cause)


def message(msg, addr):
    trigger_alarm("sensor on %s:%s" % addr)


def disconnect(addr):
    trigger_alarm("disconnect from %s:%s" % addr)


def submit(pin):
    print("Entered pin: " + pin)
    if pin == "1234":
        toggle_alarm("pin code")
    else:
        trigger_alarm("incorrect pin")


server.server_init(8080, message, disconnect)
keypad.register(submit)
GPIO.setup(alarm_light, GPIO.OUT)
GPIO.output(alarm_light, 0)

try:
    while True:
        uid = rfid.scan()
        if uid is not None:
            print("Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3], uid[4]))
            if uid == [112, 189, 195, 87, 89]:
                toggle_alarm("rfid tag")
            else:
                trigger_alarm("incorrect tag")
        server.event_loop()
except:
    keypad.cleanup()