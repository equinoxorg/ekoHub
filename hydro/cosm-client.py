import urllib2
import serial
import argparse
from datetime import datetime, timedelta, tzinfo
import time

import json

def launch():
	parser = argparse.ArgumentParser(description="UART to Cosm Bridge")

	parser.add_argument('serialport', action='store', help='Device node for serial port')
	parser.add_argument('-u', '--update_interval', default=300, action='store', type=int, help='Interval between server updates')


	args = parser.parse_args()
	return vars(args)

def main():
	args = launch()
	store = []

	# open the serial port
	ser = serial.Serial(args['serialport'], 9600)
	# create a buffer for chars
	buffer = ''
	timeout = timedelta(seconds=args['update_interval'])
	# loop infinitely
	while True:
		# get lines anything left (in buffer)
		data, buffer = get_reading(ser, buffer)
		print("Got %d lines of data" % len(data))
		for d in data:
			print("%s : %s = %d" % (d['node'], d['at'], d['value']))
		# append to store
		store = store + data
		lastsync = datetime.utcnow()
		# if more than 10 samples or if timeout
		if ((len(store) > 9) or ((datetime.utcnow() - lastsync) > timeout)):
			if(send_cosm(store)):
				# if data sent to server, empty store
				store = []
			# sync again in x seconds
			lastsync = datetime.utcnow()
		if len(store) > 500:
			# get rid of data, cosm can't handle
			store = []
			# you should dump to file perhaps?

def send_cosm(list):
	# two sets of empty variables
	weirdata = []
	forebaydata = []
	if len(list) == 0:
		return
	# collate into above
	for item in list:
		if item['node'] == 'weir':
			weirdata.append({'at':item['at'], 'value':item['value']})
		if item['node'] == 'forebay':
			forebaydata.append({'at':item['at'], 'value':item['value']})

	# create a json string
	if len(weirdata) > 0:
		jsonweir = json.dumps({'datapoints': weirdata})
		# send a http post with this data
		stat1 = httppost('http://api.cosm.com/v2/feeds/73407/datastreams/weir_water/datapoints', jsonweir)
		
	if len(forebaydata) > 0:
		jsonforebay = json.dumps({'datapoints': forebaydata})
		stat2 = httppost('http://api.cosm.com/v2/feeds/73407/datastreams/forebay_water/datapoints', jsonforebay)

	return stat1 & stat2

def httppost(url, data):
	req = urllib2.Request(url)
	req.add_header('X-ApiKey', 'CB3uqfOJSiEBbMaO0ljmwjYEoVWSAKwvb0dWWWpJaFdrVT0g')
	req.add_data(data)
	f = None
	try:
		f = urllib2.urlopen(req, timeout=20)
		print("Syncing to Cosm")
		print(url)
	except urllib2.URLError as e:
		print(e)
		return False
	if not f:
		print("No response")
		return False
	return True

def get_reading(ser, buffer):
	# loop until we receive atleast 1 newline
	while True:
		# get data and append to buffer
		buffer = buffer + ser.read(ser.inWaiting())
		# if newline in buffer
		if '\n' in buffer:
			# split by newline
			lines = buffer.split('\n')
			# last list item is any text trailing last newline
			# get everything but last line
			data = lines[:-1]
			# consider the time all above packets received as just now
			outdata = []
			recv_time = datetime.utcnow()
			for item in data:
				# seperate it all
				node, value = tuple(item.split(','))
				try:
					outdata.append({'at': recv_time.isoformat(), 'node': node, 'value' : int(value)})
				except Exception as e:
					print(e)
					pass
			# get remainder
			buffer = lines[-1]
			# return both
			return(outdata, buffer)

if __name__ == "__main__":
	main()