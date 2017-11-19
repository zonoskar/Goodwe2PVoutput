
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
      print "Logging: " + gw.to_short_string()


#---------------- End of file ------------------------------------------------
