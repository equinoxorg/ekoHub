
import cgi
import wsgiref.handlers
from dataFile import dataObject , ObjectCounter
from timeUtilities import GMT1, GMT2, TimeHandler
from modemUtilities import sensorsHandler, logHandler
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import date, datetime
import webapp2
import time
 
 
no_sensors = 8



class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.out.write("Welcome to the webpage of e.quinox's second datalogger.<br/>")
    self.response.out.write("Unfortunately the page is still undergoing development...")


 
app = webapp2.WSGIApplication([( '/' , MainPage ), 
                              ( '/sensors' , sensorsHandler),
                              ( '/log' , logHandler),
                              ( '/time' , TimeHandler)],
                                debug = True)
 
def main():
    run_wsgi_app(app)
 
if __name__ == '__main__':
  main()