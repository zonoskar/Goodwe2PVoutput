import time

class processNone :

   #--------------------------------------------------------------------------
   def __init__( self, pvoutput):
      self.m_pvoutput = pvoutput
      
           
   #--------------------------------------------------------------------------
   def reset( self):
      pass
   
   
   #--------------------------------------------------------------------------
   def processSample( self, gw):
      if self.m_pvoutput:
         self.m_pvoutput.post_data( gw)
      t = time.localtime(time.time())
      print "Logging:   " + str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2) + "h " + gw.to_short_string()


#---------------- End of file ------------------------------------------------
