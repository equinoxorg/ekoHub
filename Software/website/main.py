import cgi
import wsgiref.handlers
from dataFile import sensorReadings , ObjectCounter
from timeUtilities import GMT1, GMT2, TimeHandler
from modemHandlers import sensorsHandler, logHandler
from settingsHandlers import remoteSettingsHandler
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import date, datetime
from utility_functions import *
from userHandlers import *

import webapp2
import time
from math import pow
import jinja2
import os
import random
import urllib
 

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

default_kiosk = 'Minazi'
default_system = 'Left Solar Panel'

kiosks = ['Minazi', 'Batima', 'Kigali', 'Rugahagara']
systems = ['Left Solar Panel', 'Right Solar Panel', 'Left Battery', 'Right Battery'
, 'Left Inverter', 'Right Inverter']

# displays the Main page
class MainPage(webapp2.RequestHandler):

  def get(self):

    i = 0
    #!!!!!MAKE SURE YOU COMMENT THE LINE BELOW BEFORE DEPLOYMENT!!!
    db.delete(sensorReadings.all())
    while i < 10:
        newObject = sensorReadings()

        newObject.sampleTime  = random.randint(1, 50)
        newObject.ac_current1 = random.randint(1, 50)
        newObject.ac_current2 = random.randint(1, 50)
        newObject.ac_voltage1 = random.randint(1, 50)
        newObject.ac_voltage2 = random.randint(1, 50)

        newObject.dc_current1 = random.randint(1, 50)
        newObject.dc_current2 = random.randint(1, 50)
        newObject.dc_current3 = random.randint(1, 50)
        newObject.dc_current4 = random.randint(1, 50)



        newObject.dc_voltage1 = random.randint(1, 50)
        newObject.dc_voltage2 = random.randint(1, 50)
        newObject.dc_voltage3 = random.randint(1, 50)
        newObject.dc_voltage4 = random.randint(1, 50)
        newObject.put()

        i = i + 1

    user_name = active_user()
    active = False if (user_name == '') else True
    login = users.create_login_url(self.request.uri)
    kiosk = self.request.get('kiosk', default_value='Minazi')
    system = self.request.get('sys', default_value='Left Solar Panel')

    #Note: When user submits kiosk and system selection,
    #the parameters will be returned inside this method
    #We'll need to perform datastore query according to the 
    # parameters
    template_values = {
    	'json_data':  serialize(sensorReadings),
        'user_name': user_name,
        'active_user': active,
        'login_url': login,
        'kiosk': kiosk,
        'kiosks': kiosks,
        'systems': systems,
        'sys': system

    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

    #self.response.write("<html>kiosk = " + str(kiosk) + '<br>')
    #self.response.write("<html>tmp = " + str(system) + '<br>')

    """
    login = users.create_login_url(self.request.uri)
    if not active:
        self.redirect(login)
        if active_user():
            self.redirect('/')


    self.response.write('active: ' + str(active) + '<br>') 
    self.response.write('uri: ' + str(login)) """

  # Collects the submitted kiosk form and updates 
  # the URL parameters for graph selected before 
  # returning to the homepage
  def post(self):  
    k = self.request.get('kiosk')
    s = self.request.get('system')
    params = urllib.urlencode({'kiosk': k, 'sys': s})

    """
    self.response.write('<html><body>You wrote:<pre>')
    self.response.write( k + '<br>')
    self.response.write( s + '<br>')
    self.response.write( 'params: ' + params)
    self.response.write('</pre></body></html>')"""
    #url = '/?kiosk=' + k + '&' + 'sys=' + s
    self.redirect('/?' + params)



 
app = webapp2.WSGIApplication([( '/' , MainPage ), 
                              ( '/sensors' , sensorsHandler),
                              ( '/log' , logHandler),
                              ( '/Settings', remoteSettingsHandler),
                              ( '/login', userLoginHandler),
                              ( '/logout', LogoutPage),
                              ( '/time' , TimeHandler)],
                                debug = True)
 


def main():
    run_wsgi_app(app)
 
if __name__ == '__main__':
  main()