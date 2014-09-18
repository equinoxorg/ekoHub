import cgi
import webapp2
import json
from data import systemData
 

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
	def post(self):

		# look for the following parameters to 
		# identify where the data is coming from
		dev = cgi.escape(self.request.get('dev'))
		kiosk = cgi.escape(self.request.get('kiosk'))
		self.response.clear()

		if not dev == 'mBed':
			self.response.set_status(400)
			self.response.out.write("Device unknown<br/>")

		if not kiosk:
			self.response.set_status(400)
			self.response.out.write("No kiosk info given<br/>")

		else:
			# ensure that the value of these parameters
			# are valid
			#if dev == 'mBed' and kiosk:

				try: # try to decode json string
					data = json.loads(cgi.escape(self.request.get("data")))

					#now save the values corresponding to each system
					# to the datastore
					for key in systems:
						#self.response.write(key + ": " + systems[key] + "<br/>")
						#save data
						systemData(current=data[key]["c"], 
								voltage=data[key]["v"], 
								kiosk=kiosk,
								system=systems[key],
								timestamp= int(data["time"])).put()				

					self.response.out.write("saved sensor data")

				except ValueError, e:
					self.response.set_status(400)
					self.response.out.write("Data sent isn't a valid json string")


		#else:
			#self.error(404)
			#set_status(404, "no parameters provided")

		#	self.response.out.write("no parameters provided")






