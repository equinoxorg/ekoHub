from datetime import datetime
from datetime import timedelta
from datetime import tzinfo
from google.appengine.ext import webapp, db
import time


# this module contains time zone  information objects.
# they provide a customizable notion of time adjustment
# more information can be found from http://docs.python.org/2/library/datetime.html

# UK(London) time UTC/GMT+1
class GMT1(tzinfo):
        def utcoffset(self, dt):
            return timedelta(hours=1)
        def dst(self, dt):
            return timedelta(0)
        def tzname(self,dt):
            return "Europe/Prague"

# Rwanda(Kigali) time UTC/GMT+2
class GMT2(tzinfo):
	     def utcoffset(self, dt):
	         return timedelta(hours=2) + self.dst(dt)
	     def dst(self, dt):
	         d = datetime(dt.year, 4, 1)
	         self.dston = d - timedelta(days=d.weekday() + 1)
	         d = datetime(dt.year, 11, 1)
	         self.dstoff = d - timedelta(days=d.weekday() + 1)
	         if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
	             return timedelta(hours=1)
	         else:
	             return timedelta(0)
	     def tzname(self,dt):
	         return "GMT +2"

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


# Time server
class TimeHandler(webapp.RequestHandler):

  def get(self):
    utc = datetime.utcnow()
    

    offset = self.request.get('offset')
    UKtime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT1())
    Rwandatime = datetime.fromtimestamp(time.mktime(utc.timetuple()), GMT2())


    if (offset == '1'):
      self.response.write( str(time.mktime(UKtime.timetuple()))  )

    elif (offset == '2'):
      self.response.write( str(time.mktime(Rwandatime.timetuple()))  )

    
    else :
      self.response.write( str(time.mktime(utc.timetuple()))  )






