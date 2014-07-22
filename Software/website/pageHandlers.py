from google.appengine.ext import db
from datetime import date, datetime, time
from dataFile import remoteSettings
from timeUtilities import GMT1, GMT2, UTC
from utility_functions import active_user
from google.appengine.api import users
from dataFile import systemData
import os
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

        t = cgi.escape(self.request.get('downloading'))
        if t == '1':
            self.response.write( "1")

        else:
                # get list of datetimes in DECENDING ORDER
            q =  db.GqlQuery("SELECT DISTINCT tdate\
                              FROM systemData \
                              ORDER BY tdate DESC")

            # will contain list of unique dates in descending order
            dates = []

            # store most recent date first
            old =  datetime.date(q.get().tdate)
            dates.append(old)

            # check if any of the following dates already exist
            # in our list. the list of datetimes will have multiple
            # entries # of the same date but we want to have a list of
            # unique dates
            for p in q:
                # create date object
                newDate = datetime.date(p.tdate)

                if not (newDate == old):
                    dates.append(newDate)
                    old = newDate

            user_name = active_user()
            active = False if (user_name == '') else True
            login = users.create_login_url(self.request.uri)


            template_values = {
                'user_name': user_name,
                'active_user': active,
                'login_url': login,
                'dates': dates
            }

            template = JINJA_ENVIRONMENT.get_template('/pages/downloads.html')
            self.response.write(template.render(template_values))


class downloadingHandler(webapp2.RequestHandler):
    def get(self):
        start = cgi.escape(self.request.get('startDate'))
        end = cgi.escape(self.request.get('endDate'))
        self.response.write('<html><body>You chose:<pre>')
        self.response.write(start + ' and ' + end + '<br>')


        c = self.request.get('checkbox')
 
        #self.request.write("start = %s" % a)

        self.response.write("start = %s <br>" % start)
        self.response.write("end = %s<br>" % end)
        self.response.write( "checkbox: %s<br>" %  cgi.escape(c))

        # check first if checkbox was checked or not
        if cgi.escape(c) == '1':
            #perform a query for all kioks
            self.response.write( "checkbox: checked")

            # parse dates and convert them to 
            # datetime objects
            s = datetime.strptime(start,'%a %d %b %Y')
            e = datetime.strptime(end,'%a %d %b %Y')

            #tmax = 23, 59, 59 tmin = 00, 00, 00
            tmax = time.max
            tmin = time.min

            # set bounds on start and end datetimes
            #datetime.combine(s, tmin)
            e = datetime.combine(datetime.date(e), tmax)

            # perform query to retrieve data in selected
            # range
            q = db.Query(systemData)
            q.filter('tdate >=', s).filter('tdate <=', e)
            q.order('-tdate')

            for tmp in q:
                self.response.write(str(tmp.tdate) + '<br>')

        else:
            self.response.write( "checkbox: unchecked")
        

        self.response.write('</pre></body></html>')


