import serial

class arduinoSerial(object):
	def __init__(self):
		ports=['COM%s' % (i+1) for i in range(256)]
		for port in ports:
			print(port)
			try:
				port='COM4'
				self.port = serial.Serial('COM4',9600,timeout=0)
				print("connected to com"+port)
				break
			except (OSError,serial.SerialException):
				pass
				self.port=None
				print("No device connected")
	def write_Serial(self,byte):
		if byte!="" and byte!="0" and byte!="6" and byte!="4" and byte!="8" and byte!="2":
			s=chr(int(byte,16)).encode('utf-8')
		else:
			s=byte.encode('utf-8')
		self.port.write(s)
	def read_Serial(self):
		lineIn=""
		try:
			lineIn=self.port.readline()
			if lineIn:
				try:
					return lineIn.decode("utf-8")
				except UnicodeDecodeError:
					print("\ncan't read input\n")
					return ""
		except self.port.SerialException:
			print("data could not be read")
			return ""