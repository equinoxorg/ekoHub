import json
import random
from google.appengine.api import users
from google.appengine.ext import db
from dataFile import sensorReadings , systemData
import logging
from datetime import datetime   

# checks for active user session and returns name of user
def active_user():
    user = users.get_current_user()

    if user:
        return user.nickname()

    else:
        return ''
        
 
# converts datastore instances to a list of dictionnaries
# this list will then be accessed sequentially by the JS code
# each element will be parsed as a JSON object
# the model argument is the kind of the datastore model
def serialize(data):
    # fetch all instances of the model and sort them in ascending
    # date order : from oldest to most recent
    #allInstances = model.all().order('tdate')
    itemsList = []

    try:
        for p in data:

            d = db.to_dict(p)
            # change the date to an appropriate format which the json dump can parse
            d['tdate'] = p.tdate.isoformat()
            itemsList.append(d)
    except TypeError:
        print "PropertiedClass' object is not iterable"



    return  json.dumps(itemsList)


def generate_random_data(kiosks, systems):

    #db.delete(systemData.all())
    i = 0
    while i < 1000:
        dat = systemData()
        dat.current = float(random.uniform(0.0, 50.0)) # in mA
        dat.voltage = float(random.uniform(0.0, 240.0)) # in Volts
        dat.sampleTime = random.randint(1, 10000) # in seconds
        dat.kiosk = kiosks[random.randint(0, len(kiosks) - 1)]
        dat.system = systems[random.randint(0, len(systems) - 1)]
        #dat.put()

        i = i + 1

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

#show current dates in database
def showDates():
    # query which selects a range of dates and returns
    # a gqlQuery Object containing the filter dates
    # Note: q is a datetime.datetime object
    dates =  db.GqlQuery("SELECT DISTINCT tdate FROM systemData ORDER BY tdate ASC")
    start =  dates.get()

    dates =  db.GqlQuery("SELECT DISTINCT tdate FROM systemData ORDER BY tdate DESC")
    end = dates.get()

    logging.info( "\n")

    logging.info( "start : %s", start.tdate.strftime('%x'))
    logging.info( "end : %s", end.tdate.strftime('%x'))

    for p in dates:
        d = p.tdate
        logging.info( "%s", d)

    # find oldest and most recent dates

    logging.info( "\n")


    

