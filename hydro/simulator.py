# waterlevel sim

import random
import serial
import argparse
import time
def launch():
	parser = argparse.ArgumentParser(description="Water Level Sensor Simulator")

	parser.add_argument('serialport', action='store', help='Device node for serial port')
	
	args = parser.parse_args()
	return vars(args)

def main():
	args = launch()
	# open the serial port
	ser = serial.Serial(args['serialport'], 9600)
	while True:
		str = 'forebay,%d\n' % random.randint(0,5)
		ser.write(str)
		print(str)
		time.sleep(random.randint(0,1))
		str = 'weir,%d\n' % random.randint(0,5)
		ser.write(str)
		print(str)
		time.sleep(random.randint(5,15))
	ser.close()

if __name__=="__main__":
	main()