import cgi
import webapp2
import json
from dataFile import systemData
 

kiosks = ['kigali', 'minazi', 'batima', 'rugahagara']

# description of system labels in json string
systems = { 'ls': "Left Solar Panel",
			'rs': "Right Solar Panel",
			'lb': "Left Battery",
			'rb': "Right Battery",
			'li': "Left Inverter",
			'ri': "Right Inverter"
}

# example json string
js = "{\"ls\": {\"c\": 4.00, \"v\": 10.00},\"rs\": {\"c\": 2.00, \"v\": 3.00},\"lb\": {\"c\": 5.00, \"v\": 10.00},\"rb\": {\"c\": 2.00, \"v\": -1.00},\"li\": {\"c\": -1.00, \"v\": -1.00},\"ri\": {\"c\": 7.50, \"v\": -3.30},\"time\": 437}"
class receiveSensorValues(webapp2.RequestHandler):
	def get(self):

		# look for the following parameters to 
		# identify where the data is coming from
		dev = cgi.escape(self.request.get('dev'))
		kiosk = cgi.escape(self.request.get('kiosk'))


		# verify that all the following paramaters have 
		# been received
		if dev == 'mBed' and kiosk:


			self.response.write("not empty<br/>")
			data = json.loads(js)
			"""self.response.write("json: <br/>")
			self.response.write(str(data) +  "<br/>")
			self.response.write("ls" + str(data["ls"]) + "<br/>")
			self.response.write(str(data["rs"]) + "<br/>")
			self.response.write(str(data["lb"]) + "<br/>")
			self.response.write(str(data["rb"]) + "<br/>")
			self.response.write(str(data["li"]) + "<br/>")
			self.response.write(str(data["ri"]) + "<br/>")
			self.response.write("time: " + str(data["time"]) + "<br/>")"""

			"""systemData(current=data["rs"]["c"], 
						voltage=data["rs"]["v"], 
						kiosk=kiosk,
						system="Left Solar Panel",
						sampleTime= int(data["time"])).put()"""

			for key in systems:
				self.response.write(key + ": " + systems[key] + "<br/>")
				#save data
				systemData(current=data[key]["c"], 
						voltage=data[key]["v"], 
						kiosk=kiosk,
						system=systems[key],
						sampleTime= int(data["time"])).put()				

			self.response.write("saved sensor data")


		else:
			self.response.write("no parameters provided")






