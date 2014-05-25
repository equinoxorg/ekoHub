
import cgi
import wsgiref.handlers
from dataFile import sensorReadings , ObjectCounter
from timeUtilities import GMT1, GMT2, TimeHandler
from modemUtilities import sensorsHandler, logHandler
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from datetime import date, datetime
import webapp2
import time
from math import pow
import json
import jinja2
import os
import random
 
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
 
# converts datastore instances to a list of dictionnaries
# this list will then be accessed sequentially by the JS code
# each element will be parsed as a JSON object
# the model argument is the kind of the datastore model
def serialize(model):
    # fetch all instances of the model and sort them in ascending
    # date order : from oldest to most recent
    allInstances = model.all().order('tdate')
    itemsList = []
    for p in allInstances:

        d = db.to_dict(p)
        # change the date to an appropriate format which the json dump can parse
        #d['tdate'] = p.tdate.strftime('%Y-%m-%dT%H:%M:%S')
        convertToAnalogue(d)
        d['tdate'] = p.tdate.isoformat()
        #convertToAnalogue(d)


        itemsList.append(d)


    return  json.dumps(itemsList)


# converts the decimal readings to analogue form
def convertToAnalogue(data_instance):
    
    Vref = 5 # voltage reference
    n = 10 # number of bits
    ADCmaxValue = pow(2, n)
    #check if argument is a dictionnary
    if isinstance(data_instance, dict):
        data_instance['ac_current1'] = data_instance['ac_current1'] * (Vref / ADCmaxValue)   
        data_instance['ac_current2'] = data_instance['ac_current2'] * (Vref / ADCmaxValue)
        data_instance['ac_voltage1'] = data_instance['ac_voltage1'] * (Vref / ADCmaxValue)
        data_instance['ac_voltage2'] = data_instance['ac_voltage2'] * (Vref / ADCmaxValue)

        data_instance['dc_current1'] = data_instance['dc_current1'] * (Vref / ADCmaxValue)
        data_instance['dc_current2'] = data_instance['dc_current2'] * (Vref / ADCmaxValue)
        data_instance['dc_current3'] = data_instance['dc_current3'] * (Vref / ADCmaxValue)
        data_instance['dc_current4'] = data_instance['dc_current4'] * (Vref / ADCmaxValue)

        data_instance['dc_voltage1'] = data_instance['dc_voltage1'] * (Vref / ADCmaxValue)
        data_instance['dc_voltage2'] = data_instance['dc_voltage2'] * (Vref / ADCmaxValue)
        data_instance['dc_voltage3'] = data_instance['dc_voltage3'] * (Vref / ADCmaxValue)
        data_instance['dc_voltage4'] = data_instance['dc_voltage4'] * (Vref / ADCmaxValue)

class MainPage(webapp2.RequestHandler):

  def get(self):
    #self.response.out.write("Welcome to the webpage of e.quinox's second datalogger.<br/>")
    #self.response.out.write("Unfortunately the page is still undergoing development...")

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



    
    template_values = {
    	'json_data':  serialize(sensorReadings)

    }

    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))


 
app = webapp2.WSGIApplication([( '/' , MainPage ), 
                              ( '/sensors' , sensorsHandler),
                              ( '/log' , logHandler),
                              ( '/time' , TimeHandler)],
                                debug = True)
 





def main():
    run_wsgi_app(app)
 
if __name__ == '__main__':
  main()