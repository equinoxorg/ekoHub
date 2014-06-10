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
 

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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

    template_values = {
    	'json_data':  serialize(sensorReadings),
        'user_name': user_name,
        'active_user': active,
        'login_url': login

    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

    """
    login = users.create_login_url(self.request.uri)
    if not active:
        self.redirect(login)
        if active_user():
            self.redirect('/')


    self.response.write('active: ' + str(active) + '<br>') 
    self.response.write('uri: ' + str(login)) """
    
 
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