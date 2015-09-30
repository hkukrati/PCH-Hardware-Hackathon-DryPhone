import subprocess
import RPi.GPIO as GPIO
from pygame import mixer    

#init
status = "OK"
mixer.init()
red = 11
green = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.HIGH)


#infinite loop so that sensor is always polling 
infinite = "inf"
while infinite == "inf": 

#loop to poll pcsc_scan every second
	while status=="OK" :

		buf = subprocess.Popen("timeout 1s pcsc_scan", stdout=subprocess.PIPE, shell=True)

		(output, err) = buf.communicate()

		det = "Card inserted"

		txt = str(output)

		if "NONE" in output:
			status = "Cell"
		elif det in output:
			status = "Warning!"


	# outputs when item detected 
	#print status, "Item Detected"
	GPIO.output(red, GPIO.HIGH)
	GPIO.output(green, GPIO.LOW)

	while (status == "Warning!") or (status == "Cell"):
		if status == "Cell":
			subprocess.call(["aplay", "/media/Phone.wav"])
		else:
			subprocess.call(["aplay", "/media/Default.wav"])
		det2 = "Card removed"
	
		buf = subprocess.Popen("timeout 1s pcsc_scan", stdout=subprocess.PIPE, shell= True)
		(output, err) = buf.communicate() 	

		if det2 in output:
			status = "OK"
			GPIO.output(red, GPIO.LOW)
			GPIO.output(green, GPIO.HIGH)

	

