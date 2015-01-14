import cgi
import wsgiref.handlers
from data import systemData
from pageHandlers import remoteSettingsHandler, downloadsHandler
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import run_wsgi_app
from utility_functions import *
from userHandlers import *
from kioskHandler import *

import webapp2
from mBed.receiveSensorValues import *
from google.appengine.api import app_identity
import time
import jinja2
import os
import random
import urllib
import logging
 

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
    generate_random_data(kiosks, systems)

    #showDates()

    #check if a user is already logged in
    user_name = active_user()
    active = False if (user_name == '') else True
    login = users.create_login_url(self.request.uri)
    kiosk = self.request.get('kiosk', default_value='Minazi')
    system = self.request.get('sys', default_value='Left Solar Panel')

    filtered_data = systemData.all()
    filtered_data = filtered_data.filter("kiosk =", kiosk).filter("system =", system)
    logging.info("app id: " + app_identity.get_default_version_hostname() + "\n")
    #data.filter("kiosk = ", kiosk)

    #Note: When user submits kiosk and system selection,
    #the parameters will be returned inside this method
    #We'll need to perform datastore query according to the 
    # parameters
    template_values = {
    	'json_data':  serialize(filtered_data),
        'user_name': user_name,
        'active_user': active,
        'login_url': login,
        'kiosk': kiosk,
        'kiosks': kiosks,
        'systems': systems,
        'sys': system,
        'data': filtered_data
    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

    #self.response.write("<html>kiosk = " + str(kiosk) + '<br>')
    #self.response.write("<html>tmp = " + str(system) + '<br>')


  # Collects the submitted kiosk form and updates 
  # the URL parameters for graph selected before 
  # returning to the homepage
  def post(self):  
    k = self.request.get('kiosk')
    s = self.request.get('system')
    params = urllib.urlencode({'kiosk': k, 'sys': s})
    self.redirect('/?' + params)

app = webapp2.WSGIApplication([( '/' , MainPage ),  
                              ( '/receiveSensorValues', receiveSensorValues),
                              ( '/Settings', remoteSettingsHandler),
                              ( '/login', userLoginHandler),
                              ( '/logout', LogoutPage),
                              ( '/Downloads', downloadsHandler),
                              ( '/Kiosks', kioskHandler)],
                                debug = True)
 


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(app)
 
# The condition below will be true if this file isn't imported
# anywhere
# we only want this application to run we want to
# execute this code as the main program
if __name__ == '__main__':
  main()