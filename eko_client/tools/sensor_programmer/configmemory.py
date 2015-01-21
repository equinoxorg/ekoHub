import struct

class ConfigMemory(object):
	"""This class represents the config memory
	For mapping see:
	https://github.com/equinoxorg/eko-sensor-firmware/blob/master/board/p24_board.h
	Note that modbus words are 16bit, and EEPROM words are 8bits
	"""
	
	CFG_EE_MBADDR = 0x00
	CFG_EE_MBCLS = 0x01
	CFG_EE_ADC_ISEL = 0x02
	CFG_EE_ADC_REPT = 0x03
	CFG_EE_ADC_SAMP = 0x04
	CFG_EE_ADC_WAIT = 0x05
	CFG_EE_I2C_CHIP = 0x06
	CFG_EE_LOCK_HI = 0x10
	CFG_EE_LOCK_LO = 0x11
	
	def __init__(self, mbaddr = 0x01, mbcls = 0, adcinpsel = 0, adcrepeat = 0, \
	adcsampleint = 0, adcwait = 0, i2cchip = 0):
		self.mbaddr = mbaddr
		self.mbcls = mbcls
		self.adcinpsel = adcinpsel
		self.adcrepeat = adcrepeat
		self.adcsampleint = adcsampleint
		self.adcwait = adcwait
		self.i2cchip = 0
	
	def encode(self):
		"""Encode config data to a byte array"""
		# the bytes are being packed into two word
		bytes = [self.mbaddr, self.mbcls, self.adcinpsel, self.adcrepeat, \
		self.adcsampleint, self.adcwait, self.i2cchip, 0]
		
		# use the struct module to encode these bytes. Count must be even!
		bytestr = struct.pack('>'+'B'*len(bytes), *bytes)
		# the above made a byte string, now we convert this back into 16bit ints
		words = struct.unpack('>'+'H'*(len(bytes)/2), bytestr)
		return words
		
	def decode(self, array):
		"""Converts 16bit ints to a object"""
		if len(array) != 4:
			raise ValueError("Array of wrong size")
		bytestr = struct.pack('>'+'H'*len(array), *array)
		bytearray = struct.unpack('>'+'B'*(2*len(array)), bytestr)
		print(bytearray)
		self.mbaddr = bytearray[0]
		self.mbcls = bytearray[1]
		self.adcinpsel = bytearray[2]
		self.adcrepeat = bytearray[3]
		self.adcsampleint = bytearray[4]
		self.adcwait = bytearray[5]
		self.i2cchip = bytearray[6]
		# last element is padding
	
	def prettyprint(self):
		print("Printing Configuration")
		print("-"*15)
		print("Modbus Address: \t (0x%x) \t %d" % (self.mbaddr, self.mbaddr))
		print("Modbus Device Class: \t 0x%x" % self.mbcls)
		print("ADC Input Selection: \t 0x%x" % self.adcinpsel)
		print("ADC Repeat Count: \t (0x%x) \t %d times" % (self.adcrepeat, self.adcrepeat))
		print("ADC Sample Interval: \t (0x%x) \t %d ms" % (self.adcsampleint, self.adcsampleint))
		print("ADC Wait: \t\t (0x%x) \t %d ms" % (self.adcwait, self.adcwait))
		print("I2C Chip Selection: \t 0x%x" % self.i2cchip)
		print("")
	
	def _adcinpsel_to_list(self):
		# 6 ADC channels
		lst = [0, 0, 0, 0, 0, 0]
		# each channel corresponds to a bit of the adcinpsel register
		# channel 0 is LSB and channel 5 is bit 6, eg:
		for i in range(6):
			# and op checks if bit is set
			if ((i & self.adcinpsel) == 0):
				# lst has AN0 at start, AN5 at end
				lst[5-i] = False
			else:
				lst[5-i] = True
		return lst
	
	def _i2cchipsel_to_string(self):
		pass
	
	def print_adcinpsel(self):
		print("ADC Channel Selection:")
		print("AN0\tAN1\tAN2\tAN3\tAN4\tAN5")
		adclist = self._adcinpsel_to_list()
		print("%s\t%s\t%s\t%s\t%s\t%s" % tuple(["*" if x==True else "-" for x in adclist]))
		print("")

if __name__=="__main__":
	c1 = ConfigMemory()
	c2 = ConfigMemory()
	x = c1.encode()
	print(x)
	c2.decode(x)
	c1.prettyprint()
	c2.prettyprint()
	c1.print_adcinpsel()
	c1.adcinpsel = int('00001011', 2)
	c1.print_adcinpsel()