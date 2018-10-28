
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import socket							   #Import socket library

GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering

TRIG = 23                                  #pin 23 as trig
ECHO = 24                                  #pin 24 as echo
MOVEMENT = 25                              #pin 25 to output radar sensor

print("Starting alarm")
time.sleep(15)
print("Alarm started")

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(MOVEMENT, GPIO.IN)

# with socket.socket() as s:			   #connect to server pi to send the detection message
#     s.connect(("serverip", 8080))

while True:

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  time.sleep(1)							   #Test sleep

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse

  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  state = GPIO.input(MOVEMENT)
                                                                #Test if statements to see if the sensors are working correctly
  # if distance < 10.0:
  #   print("inbreker afstand" + (time.strftime("%H:%M:%S")))
  #
  #   GPIO.cleanup()
  #   break;
  #
  # if state == 1:
  #     print("Inbreker radar" + (time.strftime("%H:%M:%S")))
  #     GPIO.cleanup()
  #     break;

  if distance < 10.0 or state ==1:
    # s.send(b"True")                     #Send True as message to server pi when intruder is detected
