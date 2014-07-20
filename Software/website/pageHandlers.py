from google.appengine.ext import db
from datetime import date, datetime
from dataFile import remoteSettings
from timeUtilities import GMT1, GMT2, UTC
from utility_functions import active_user
from google.appengine.api import users
from dataFile import systemData
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
        user_name = active_user()
        active = False if (user_name == '') else True
        login = users.create_login_url(self.request.uri)

        template_values = {
            'user_name': user_name,
            'active_user': active,
            'login_url': login,
        }
        template = JINJA_ENVIRONMENT.get_template('/pages/settings.html')
        self.response.write(template.render(template_values))
    

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

class downloadsHandler(webapp2.RequestHandler):
    def get(self):


        user_name = active_user()
        active = False if (user_name == '') else True
        login = users.create_login_url(self.request.uri)

        # perform a datastore query to find the oldest
        # and most recent dates

             #       'startDate': start,
            #'endDate': end

        template_values = {
            'user_name': user_name,
            'active_user': active,
            'login_url': login
        }

        template = JINJA_ENVIRONMENT.get_template('/pages/downloads.html')
        self.response.write(template.render(template_values))


class downloadingHandler(webapp2.RequestHandler):
    def get(self):
        start = self.request.get('startDate')
        end = self.request.get('endDate')
        self.response.write('<html><body>You chose:<pre>')
        self.response.write(start + ' and ' + end + '<br>')


        # get the first elements of each query
        s =  db.GqlQuery("SELECT DISTINCT tdate\
                          FROM systemData \
                          ORDER BY tdate ASC").get()

        e =  db.GqlQuery("SELECT DISTINCT tdate\
                          FROM systemData \
                          ORDER BY tdate DESC").get()
        a = "caca"
        #self.request.write("start = %s" % a)
        self.response.write("start = %s <br>" % s.tdate.strftime('%x'))
        self.response.write("end = %s<br>" % e.tdate.strftime('%x'))

        self.response.write('</pre></body></html>')


