from google.appengine.ext import db
from datetime import date, datetime
from dataFile import remoteSettings
from timeUtilities import GMT1, GMT2, UTC
import os, time
import cgi
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class remoteSettingsHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('/pages/remoteParameters.html')
        self.response.write(template.render())
    

    def post(self):
        # delete previous settings and update
        # with new settings
        db.delete(remoteSettings.all())

        m = remoteSettings()

        # fetch content written from user
        sampleTime = cgi.escape(self.request.get('SampleTime', '0'))
        watchdogTime = cgi.escape(self.request.get('WatchdogTime', '0'))
        noLines = cgi.escape(self.request.get('nolines', '0'))
        startOfDay = cgi.escape(self.request.get('startDay', '0'))
        endOfDay = cgi.escape(self.request.get('endDay', '0'))

        # save settings to datastore
        m.sampleTime = sampleTime
        m.watchdogTime = watchdogTime
        m.noLines = noLines
        m.startOfDay = startOfDay
        m.endOfDay = endOfDay
        m.put()

        template = JINJA_ENVIRONMENT.get_template('/pages/savedParameters.html')

        template_values = {
        	'sampleTime': sampleTime,
        	'watchdogTime': watchdogTime,
        	'noLines': noLines,
        	'startOfDay': startOfDay,
        	'endOfDay': endOfDay

        }
        self.response.write(template.render(template_values))


