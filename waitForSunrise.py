import datetime
import time

class Sunrise :

MEANSUNRISEPERMONTH = [ 7, 7, 6, 5, 5, 4, 4, 5, 5, 6, 7, 7 ]

   #--------------------------------------------------------------------------
   def __init__( self):
   #
       self.month = 0

      
   #--------------------------------------------------------------------------
   def wait( self):
   #
       thisMonth = datetime.date.today().month - 1
       interval = (24 - datetime.time().hour) * 60 * 60
       interval +=(60 - datetime.time().minute) * 60
       interval += MEANSUNRISEPERMONTH[thisMonth] * 60 * 60;
       
       print "sunrise: " + str(MEANSUNRISEPERMONTH[thisMonth])
       print "waiting " + str(interval) + " secs"
       
       
       
       time.sleep(interval)
   

