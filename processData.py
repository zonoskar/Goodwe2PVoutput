import logging

class processData :
   BUFFERING = 'BUFFERING'
   LOG_PREV_SAME = 'LOG_PREV_SAME'
   LOG_PREV_DIFF = 'LOG_PREV_DIFF'
   INTERPOLATE = 'INTERPOLATE'

   #--------------------------------------------------------------------------
   def __init__( self, pvoutput):
   # Processing class. This class converts the data from the GoodWe logging
   # frequency of once every 10 min, to the log interval of 5 min of PVOutput
   # by interpolating.
   #
      self.m_switch = {self.BUFFERING:     self.buffering,
                       self.LOG_PREV_SAME: self.logging,
                       self.LOG_PREV_DIFF: self.logging,
                       self.INTERPOLATE:   self.interpolate}
      self.m_state = self.BUFFERING
      self.m_prev_gw = None
      self.m_pvoutput = pvoutput


   #--------------------------------------------------------------------------
   def state_to_string( self):
   # Converts the state to a string
   #
      return self.m_state


   #--------------------------------------------------------------------------
   def update_state( self, gw):
   # Updates the state.
   #
      if not self.m_prev_gw:
         self.m_state == self.BUFFERING
      else:
         if gw.is_identical( self.m_prev_gw):
            self.m_state = self.LOG_PREV_SAME
         else:
            if self.m_state == self.LOG_PREV_SAME:
               self.m_state = self.INTERPOLATE
            else:
               self.m_state = self.LOG_PREV_DIFF


   #--------------------------------------------------------------------------
   def logging( self, gw):
   # Processes the LOGGING state. This logs the m_prev_gw data
   #
      if self.m_pvoutput:
         self.m_pvoutput.post_data( self.m_prev_gw)
      logging.info("Logging: " + self.m_prev_gw.to_short_string())


   #--------------------------------------------------------------------------
   def buffering( self, gw):
   # Processes the BUFFERING state. Basically does nothing.
   #
      logging.info("Buffering: " + gw.to_short_string())


   #--------------------------------------------------------------------------
   def interpolate( self, gw):
   # Interpolates the current and the previous sample by using linear interpolation.
   #
      gw1 = gw.interpolate( self.m_prev_gw)
      if self.m_pvoutput:
         self.m_pvoutput.post_data( gw1)
      logging.info("Interpolate: " + gw1.to_short_string())
      self.m_state = self.LOG_PREV_DIFF


   #--------------------------------------------------------------------------
   def reset( self):
   # Resets the processing class when the inverter goes offline and logs the
   # last sample.
   #
      # Flush the last dat apoint to PVOutput
      if self.m_prev_gw:
         self.logging( self.m_prev_gw)
      self.m_state = self.BUFFERING
      self.m_prev_gw = None


   #--------------------------------------------------------------------------
   def processSample( self, gw):
   # This method processes the sample by calling the method associated with the
   # current state
   #
      self.update_state( gw)
      self.m_switch[self.m_state](gw)

      self.m_prev_gw = gw

