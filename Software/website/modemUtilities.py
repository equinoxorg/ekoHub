from google.appengine.ext import db
from datetime import date, datetime
from dataFile import FileObject, sensorReadings
from timeUtilities import GMT1, GMT2, UTC
import os, time
import cgi
import webapp2


class sensorsHandler(webapp2.RequestHandler):

	def get(self):
		utc = datetime.utcnow()
		self.response.write("current date " + utc.strftime("%A %d %B %Y %I:%M%p") + '<br/>')

		UKTime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT1())
		RwandaTime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT2())

		self.response.write("UK Time: " + UKTime.ctime());
		self.response.write("<br/>UK Timestamp " + str(time.mktime(UKTime.timetuple())) )
		self.response.write("<br/>Rwanda Time: " + RwandaTime.ctime() +  "<br/>");

		data_query = db.GqlQuery("SELECT * "
								 "FROM sensorReadings "
								 "ORDER BY tdate DESC LIMIT 1"
                            	)

		self.response.out.write("<br/>Number of rows: " + str( data_query.count()) )


		newObject = sensorReadings()
		newObject.put()


	def post(self):
		# get data from mbed and write it to a buffer
		buf = self.request.get('e.quinoxsensors') 

		# convert data to an array by detecting whitespace
		array = buf.split(' ')

		utc = datetime.utcnow()
		UKtime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT1())


		# query on all properties
		data_query = db.GqlQuery("SELECT * "
								 "FROM sensorReadings "
								)
		count = data_query.count()

		if not (buf == ''):
			i = 0

			for index, item in enumerate(array):
				i = i+1

				if( i%12 == 0):
					count = count + 1

					newObject = sensorReadings(tdate = UKtime)
					newObject.sampleTime  = int(array[index - 12])
					newObject.ac_current1 = int(array[index - 11])
					newObject.ac_current2 = int(array[index - 10])
					newObject.ac_voltage1 = int(array[index - 9])
					newObject.ac_voltage2 = int(array[index - 8])

					newObject.dc_current1 = int(array[index - 7])
					newObject.dc_current2 = int(array[index - 6])
					newObject.dc_current3 = int(array[index - 5])
					newObject.dc_current4 = int(array[index - 4])

					newObject.dc_voltage1 = int(array[index - 3])
					newObject.dc_voltage2 = int(array[index - 2])
					newObject.dc_voltage3 = int(array[index - 1])
					newObject.dc_voltage4 = int(array[index])
					newObject.no = count
					newObject.put()

			tmp = UKtime.strftime("%A %d %B %Y %I:%M%p")
			self.response.write('Google App Engine Web server received file on ' + tmp+ ' (UKTime)')

class logHandler(webapp2.RequestHandler):
	def get(self):
		query = db.GqlQuery("SELECT * "
							"FROM FileObject "
							"ORDER BY tdate DESC LIMIT 1"
							)

		if query is not None:
			for tmp in query:
				self.response.write('log : <br/>' + cgi.escape(tmp.text))

	def post(self):
		buf = self.request.get('e.quinoxlog')

		if not ( buf == ''):
			UKtime = datetime.fromtimestamp(time.mktime(datetime.utcnow().timetuple()), GMT1())
			newObject = FileObject(text = buf, tdate = UKtime)
			newObject.put()

			_time = UKtime.strftime("%A %d %B %Y %I:%M%p")
			self.response.write('Google App Engine Web server received file on ' + _time + ' (UKTime)')






