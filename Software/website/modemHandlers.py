from google.appengine.ext import db
from datetime import date, datetime
from dataFile import log, sensorReadings, remoteSettings
from timeUtilities import GMT1, GMT2, UTC
import os, time
import cgi
import webapp2
import jinja2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def store_kiosk_data(data, kiosk):
    # convert data to an array by detecting whitespace
    array = data.split(' ')

    # query on all properties
    data_query = db.GqlQuery("SELECT * "
        "FROM sensorReadings "
    )
    count = data_query.count()

    if not (data == ''):
        i = 0

    for index, item in enumerate(array):
        i = i+1

    if(i%12 == 0):
        count = count + 1

    newObject = sensorReadings(tdate = UKtime, kiosk = kiosk)
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
        #buf = self.request.get('e.quinoxsensors') 

        kiosks = ['kigali', 'minazi', 'batima', 'rugahagara']
        dat = []

        utc = datetime.utcnow()
        UKtime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT1())

        # collect data coming from any of the kiosks
        for i in range(0,len(kiosks)):
            dat = self.request.get(kiosks[i])
            store_kiosk_data(dat, kiosks[i])

        if not (dat == ''):
            tmp = UKtime.strftime("%A %d %B %Y %I:%M%p")
            self.response.write('Google App Engine Web server received file on ' + tmp+ ' (UKTime)')

# allows mBed to fetch remote settings
class GetSettings(webapp2.RequestHandler):
    def get(self):

        # fetch remote settings from database
        result = remoteSettings.get()
        d = result.to_dict()
        
        # convert data to json format and send to mBed
        self.response.write(json.dumps(d))



# this handler saves all the log dat sent from the mBed.
# The name of the kiosk will be specified in the log
class logHandler(webapp2.RequestHandler):
    def get(self):
        query = db.GqlQuery("SELECT * "
        "FROM log "
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


class remoteSettingsHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('remoteParameters.html')
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

        template = JINJA_ENVIRONMENT.get_template('savedParameters.html')

        template_values = {
        	'sampleTime': sampleTime,
        	'watchdogTime': watchdogTime,
        	'noLines': noLines,
        	'startOfDay': startOfDay,
        	'endOfDay': endOfDay

        }
        self.response.write(template.render(template_values))


