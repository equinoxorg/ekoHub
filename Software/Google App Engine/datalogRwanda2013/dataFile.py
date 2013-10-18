from google.appengine.ext import db

default_entity_name = 'Sensor Values'

#This file contains the different objects
# that can be stored in the database

class ObjectCounter(db.Model):
  count = db.IntegerProperty()

class FileObject(db.Model):
  text = db.TextProperty()
  tdate = db.DateTimeProperty(auto_now_add=False)
 
 

class dataObject(db.Model):

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

  
  tdate = db.DateTimeProperty(auto_now_add=False)
  
 
  # create parent key to ensure that all objects are of the same kind
def object_key( object_name = default_entity_name):
  return db.Key.from_path('Measurements' ,  object_name)