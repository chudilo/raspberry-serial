#print("Hello, Pi!")

import RPi.GPIO as GPIO
import time

import serial

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)


outputPin = 21
input_pins = (26, 19, 13, 6, 5)
#blinkDelay = 0.5
#ledOn = True
ledPin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(outputPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

for pin in input_pins:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(outputPin, GPIO.HIGH)

def get_state(input_pins):
	return [GPIO.input(pin) for pin in input_pins]

def drebezg(new_state, input_pins):
	for i in range(5):
		if [GPIO.input(pin) for pin in input_pins] != new_state:
			return False
		time.sleep(0.003)
	return True

def get_num_from_state(new_state):
	num = 0
	for i in range(len(new_state)):
		num |= new_state[i] << i
	return num

try:
	state = [GPIO.input(pin) for pin in input_pins]
	#print("state", state)
	GPIO.output(ledPin, GPIO.HIGH)
	while True:
		new_state = [GPIO.input(pin) for pin in input_pins]
		if state != new_state:
			if drebezg(new_state, input_pins):
				#print("new_state", new_state)
				num = (get_num_from_state(new_state)+50).to_bytes(1, 'big') + '\n'.encode('ascii')
				state = new_state
				print(num)
				ser.write(num)
				#ser.write(b'data\n')
	#time.sleep(0.5)
	#GPIO.output(ledPin, ledOn)
	#ledOn = not ledOn
	#time.sleep(blinkDelay)
except Exception as e:
	print(e)
finally:
	GPIO.cleanup()
