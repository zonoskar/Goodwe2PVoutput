
class processData :
   BUFFERING = 'BUFFERING'
   LOG_PREV_SAME = 'LOG_PREV_SAME'
   LOG_PREV_DIFF = 'LOG_PREV_DIFF'
   INTERPOLATE = 'INTERPOLATE'

   #--------------------------------------------------------------------------
   def __init__( self, pvoutput):
   # Processing class. This class converts the data from the Goodwe logging
   # frequency of once every 10 min, to the log interval of 5 min of PVoutput
   # by interpolating.
   #
      self.m_switch = {self.BUFFERING:     self.buffering,
                       self.LOG_PREV_SAME: self.logging,
                       self.LOG_PREV_DIFF: self.logging,
                       self.INTERPOLATE:   self.interpolate}
      self.m_state = self.BUFFERING                      
      self.m_prev_sample = None
      self.m_pvoutput = pvoutput
      
      
   #--------------------------------------------------------------------------
   def state_to_string( self):
   # Converts the state to a string
   #
      return self.m_state
      
      
   #--------------------------------------------------------------------------
   def update_state( self, sample):
   # Updates the state.
   #
      if not self.m_prev_sample:
         self.m_state == self.BUFFERING
      else:
         if sample.is_identical( self.m_prev_sample):
            self.m_state = self.LOG_PREV_SAME
         else:
            if self.m_state == self.LOG_PREV_SAME:
               self.m_state = self.INTERPOLATE
            else:
               self.m_state = self.LOG_PREV_DIFF


   #--------------------------------------------------------------------------
   def logging( self, sample):
   # Processes the LOGGING state. This logs the m_prev_sample data
   #
      if self.m_pvoutput:
         self.m_pvoutput.post_data( self.m_prev_sample)
      print "Logging: " + self.m_prev_sample.to_short_string()
      
      
   #--------------------------------------------------------------------------
   def buffering( self, sample):
   # Processes the BUFFERING state. Basically does nothing.
   #
      print "Buffering: " + sample.to_short_string()
      
      
   #--------------------------------------------------------------------------
   def interpolate( self, sample):
   # Interpolates the current and the previous sample by using linear interpolation.
   #
      sample1 = sample.interpolate( self.m_prev_sample)
      if self.m_pvoutput:
         self.m_pvoutput.post_data( sample1)
      print "Interpolate: " + sample1.to_short_string()
      self.m_state = self.LOG_PREV_DIFF

      
   #--------------------------------------------------------------------------
   def reset( self):
   # Resets the processing class when the inverter goes offline and logs the
   # last sample.
   #
      # Flush the last dat apoint to PVoutput
      if self.m_prev_sample:
         self.logging( self.m_prev_sample)
      self.m_state = self.BUFFERING 
      self.m_prev_sample = None
   
   
   #--------------------------------------------------------------------------
   def processSample( self, sample):
   # This method processes the sample by calling the method associated with the
   # current state
   #
      self.update_state( sample)
      self.m_switch[self.m_state](sample)
      
      self.m_prev_sample = sample


#---------------- End of file ------------------------------------------------
