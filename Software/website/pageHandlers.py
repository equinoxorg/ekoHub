from google.appengine.ext import db
from datetime import date, datetime, time
from data import remoteSettings, systemData
from timeUtilities import GMT1, GMT2, UTC
from utility_functions import active_user
from google.appengine.api import users
import os
import cgi
import webapp2
import jinja2
import sys
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class remoteSettingsHandler(webapp2.RequestHandler):
    def get(self):

        dev = cgi.escape(self.request.get('dev'))


        #check if mBed is requesting data from this page
        if dev == 'mBed':

            try:
                # get remote settings
                q = db.Query(remoteSettings).get()

                # Convert them to a json object
                json_data = {}
                json_data['sampleTime'] = q.sampleTime
                json_data['watchdogTimer'] = q.watchdogTimer
                json_data['noLines'] = q.noLines
                json_data['dayStart'] = q.startOfDay
                json_data['dayEnd'] =  q.endOfDay
                #json_data['uploadRate']
                #json_data['downloadRate']
                
                self.response.write(json.dumps(json_data))

            # Set HTTP status code
            except:
                self.error(404)
                self.response.write('couldn\'t find data')



        # display the web page
        else:
            user_name = active_user()
            active = False if (user_name == '') else True
            login = users.create_login_url(self.request.uri)

            # get list of hours from 00 to 24
            hours = []
            for i in range(0, 25):
                hours.append("%02d" % i)

            #get list of minutes from 00 to 59
            mins = []
            for i in range(0, 60):
                mins.append("%02d" % i)

            template_values = {
                'user_name': user_name,
                'active_user': active,
                'login_url': login,
                'saved': False,
                'hours': hours,
                'mins': mins
            }
            template = JINJA_ENVIRONMENT.get_template('/pages/settings.html')
            self.response.write(template.render(template_values))

        
    
    #submission of control settings form
    def post(self):

        user_name = active_user()
        active = False if (user_name == '') else True
        login = users.create_login_url(self.request.uri)


        # delete previous settings and update
        # with new settings. Note: Form validation is already done
        # in Javascript
        db.delete(remoteSettings.all())

        # Create a new settings object
        m = remoteSettings()

        # fetch user selecting and save it to database
        sampleRate = cgi.escape(self.request.get('sampleRate', '10'))
        #startOfDay = cgi.escape(self.request.get('startDay', '06:30'))
        startHour =  cgi.escape(self.request.get('startHour', 06))
        startMins =  cgi.escape(self.request.get('startMins', 30))

        endHour =  cgi.escape(self.request.get('endHour', 17))
        endMins =  cgi.escape(self.request.get('endMins', 00))


        #endOfDay = cgi.escape(self.request.get('endDay', '18:00'))
        samplingFreq = cgi.escape(self.request.get('samplingFreq', 10000))
        uploadRate = cgi.escape(self.request.get('uploadRate', 60))



        # save settings to datastore
        m.sampleRate = int(sampleRate)
        

        m.startOfDay = startHour + ':' + startMins

        m.endOfDay = endHour + ':' + endMins
        m.samplingFreq = int(samplingFreq)
        m.uploadRate = int(uploadRate)

        m.put()

        template = JINJA_ENVIRONMENT.get_template('/pages/settings.html')

        template_values = {
            'user_name': user_name,
            'active_user': active,
            'login_url': login,
            'saved': True
        }
        self.response.write(template.render(template_values))

        logging.info("sampleRate = %s \n" % sampleRate)
        logging.info("startOfDay = %s \n" % (startHour + ':' + startMins))
        logging.info("endOfDay = %s \n" % (endHour + ':' + endMins)) 
        logging.info("samplingFreq = %s \n" % samplingFreq)
        logging.info("uploadRate = %s \n" % uploadRate)

class downloadsHandler(webapp2.RequestHandler):
    def get(self):

        noDates = False
        errmsg = ''

        try:
            # get list of datetimes in DECENDING ORDER
            q =  db.GqlQuery("SELECT DISTINCT tdate\
                            FROM systemData \
                            ORDER BY tdate DESC")

            # Container of unique dates 
            dates = []

        
            # add most recent date first to the list
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

        except :
            noDates = True
            errmsg = 'There\'s no data to download. Come back ' \
            'another time'


        user_name = active_user()
        active = False if (user_name == '') else True
        login = users.create_login_url(self.request.uri)


        template_values = {
            'user_name': user_name,
            'active_user': active,
            'login_url': login,
            'dates': dates,
            'noDates': noDates,
            'errmsg': errmsg
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

        

    # fetch data from datastore based on the given parameters
    # return the data in a csv format
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
