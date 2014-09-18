import logging

from google.appengine.ext import db

default_entity_name = 'Sensor Values'
default_kiosk_name = "Minazi"


#Note if you want to change the types of any properties
#(i.e from int to float), you need to clear the database
# before as you may set the old values of the datastore
# to a different type

class systemData(db.Model):
  current = db.FloatProperty(default=0.000)
  voltage = db.FloatProperty(default=0.000)
  kiosk = db.StringProperty(default="Minazi")
  system = db.StringProperty(default="Left Solar Panel")
  timestamp = db.IntegerProperty(default=0) # exact datetime at which samples were taken
  tdate = db.DateTimeProperty(auto_now_add=True) # date at which data has been received
  
# Only one instance of the settings will be saved in the database and will
# be regularly updated as users will change the settings. So this object
# shouldn't affect storage limit.
class remoteSettings(db.Model):
  sampleTime  = db.StringProperty(default='600') 
  watchdogTimer = db.StringProperty(default='40')
  #noLines = db.StringProperty('10')
  startOfDay = db.StringProperty(default='6:00')
  endOfDay = db.StringProperty(default='18:00')
  samplingFreq = db.IntegerProperty(default=30000)
  #uploadRate = 
 
  # create parent key to ensure that all objects are of the same kind
def object_key( object_name = default_entity_name):
  return db.Key.from_path('Measurements' ,  object_name)