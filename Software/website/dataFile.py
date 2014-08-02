import logging

from google.appengine.ext import db

default_entity_name = 'Sensor Values'
default_kiosk_name = "Minazi"

#This file contains the different objects
# that can be stored in the database

class ObjectCounter(db.Model):
  count = db.IntegerProperty()

class log(db.Model):
  text = db.TextProperty()
  tdate = db.DateTimeProperty(auto_now_add=False)
 
class sensorReadings(db.Model):

  kiosk = db.StringProperty(default=default_kiosk_name)
  sampleTime = db.IntegerProperty(default=0)
  # from the AC board
  ac_current1 = db.IntegerProperty(default=0)
  ac_current2 = db.IntegerProperty(default=0)
  ac_voltage1 = db.IntegerProperty(default=0)
  ac_voltage2 = db.IntegerProperty(default=0)

  # from the DC board
  dc_current1 = db.IntegerProperty(default=0)
  dc_current2 = db.IntegerProperty(default=0)
  dc_current3 = db.IntegerProperty(default=0)
  dc_current4 = db.IntegerProperty(default=0)

  dc_voltage1 = db.IntegerProperty(default=0)
  dc_voltage2 = db.IntegerProperty(default=0)
  dc_voltage3 = db.IntegerProperty(default=0)
  dc_voltage4 = db.IntegerProperty(default=0)
  no = db.IntegerProperty()

  tdate = db.DateTimeProperty(auto_now_add=True)

#Note if you want to change the types of any properties
#(i.e from int to float), you need to clear the database
# before as you may set the old values of the datastore
# to a different type

class systemData(db.Model):
  current = db.FloatProperty(default=0.000)
  voltage = db.FloatProperty(default=0.000)
  kiosk = db.StringProperty(default="Minazi")
  system = db.StringProperty(default="Left Solar Panel")
  sampleTime = db.IntegerProperty(default=0)
  tdate = db.DateTimeProperty(auto_now_add=True)
  
# Only one instance of the settings will be saved in the database and will
# be regularly updated as users will change the settings. So this object
# shouldn't affect storage limit.
class remoteSettings(db.Model):
  sampleTime  = db.StringProperty('5')
  watchdogTimer = db.StringProperty('5')
  noLines = db.StringProperty('10')
  startOfDay = db.StringProperty('8:30')
  endOfDay = db.StringProperty('17:50')
 
  # create parent key to ensure that all objects are of the same kind
def object_key( object_name = default_entity_name):
  return db.Key.from_path('Measurements' ,  object_name)