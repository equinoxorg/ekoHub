import json
from google.appengine.api import users
from google.appengine.ext import db

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


