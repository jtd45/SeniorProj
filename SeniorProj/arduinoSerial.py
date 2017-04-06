class arduinoSerial(object):
	def __init__(self):
		ports=['COM%s' % (i+1) for i in range(256)]
		for port in ports:
			try:
				self.port = serial.Serial(port,9600,timeout=0)
				print("connected to com"+port)
				break
			except (OSError,serial.SerialException):
				pass
				self.port=None
				print("No device connected")
	def write_Serial(self,string):
		print(string)
		self.port.write(string.encode("Ascii"))
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
