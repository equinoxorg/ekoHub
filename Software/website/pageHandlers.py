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
import sys
import logging


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


        # get list of datetimes in DECENDING ORDER
        q =  db.GqlQuery("SELECT DISTINCT tdate\
                          FROM systemData \
                          ORDER BY tdate DESC")

        # will contain list of unique dates in descending order
        dates = []

        # store most recent date first
        latest =  datetime.date(q.get().tdate)
        dates.append(latest)

        # check if any of the following dates already exist
        # in our list. the list of datetimes will have multiple
        # entries # of the same date but we want to have a list of
        # unique dates
        for p in q:
            # create date object
            newDate = datetime.date(p.tdate)

            if not (newDate == latest):
                dates.append(newDate)
                latest = newDate

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

        # check if user submitted the download form
        down = cgi.escape(self.request.get('downloading'))

        if down == '1':

            # retrieve form arguments
            start = cgi.escape(self.request.get('startDate'))
            end = cgi.escape(self.request.get('endDate'))
            c = cgi.escape(self.request.get('checkbox'))


            #self.response.out.write( "1389979974")

            buf = self.fetch_data(c, start, end)

            # write download content into a buffer
            size  = 56  

            # clear all data written to the output stream
            self.response.clear()

            # set HTTP headers to notify server of download
            self.response.headers["Content-Type"] = "text/csv"
            self.response.headers["Cache-Control"] = "no-cache"
            self.response.headers["Content-Disposition"] = "attachment; filename=kioskData.csv"
            #self.response.headers["Content-Length"] = size
            self.response.headers["Content-Transfer-Encoding"] = "binary"
            self.response.headers["Pragma"] = "no-cache"
            self.response.write(buf)

        else:
            logging.info("No download\n")

        

    # fetch data to download based on the given parameters
    # return the data in an excel format
    def fetch_data(self, c, start , end):
        logging.debug('fetch download data')

        if c == '1':
            logging.info('All kiosks selected\n')

            # parse dates and convert them to 
            # datetime objects
            s = datetime.strptime(start,'%a %d %b %Y')
            e = datetime.strptime(end,'%a %d %b %Y')

            #tmax = 23, 59, 59 tmin = 00, 00, 00
            tmax = time.max
            tmin = time.min

            # set bounds on start and end datetimes
            e = datetime.combine(datetime.date(e), tmax)

            # perform query to retrieve data in selected
            # range
            q = db.Query(systemData)
            q.filter('tdate >=', s).filter('tdate <=', e)
            q.order('tdate').order('kiosk').order('system') 

            # create empty buffer that will contain data
            buf = 'date, time, kiosk, system, current, voltage, sample time\n'

            logging.info('traversing filtered data')

            for tmp in q.run():
                # get date
                d = (tmp.tdate).date().strftime('%d/%m/%y')
                #get time
                t = (tmp.tdate).time().strftime('%H:%M')

                #add data to buffer
                buf = buf + "%s, %s, %s, %s, %s, %s, %s\n" % (d, t, tmp.kiosk,\
                tmp.system, tmp.voltage, tmp.current, tmp.sampleTime)

            logging.info('return buffer')
            return buf 







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


