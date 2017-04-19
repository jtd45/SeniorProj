import serial
import msvcrt
import time
from arduinoSerial import arduinoSerial

if __name__=='__main__':
	port=arduinoSerial()
	allowed="46824"
	while(1):
		input_raw=msvcrt.getch()
		input=input_raw.decode("utf-8")
		if input in allowed:
			print(input)
			port.write_Serial(input)
			time.sleep(.5)