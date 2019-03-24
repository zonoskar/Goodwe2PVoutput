import numpy as np
import goodweSample
import copy
import time

class processData2 :

   funcs = { 'vpv0': goodweSample.goodweSample.get_vpv0,\
             'vpv1': goodweSample.goodweSample.get_vpv1,\
             'ipv0': goodweSample.goodweSample.get_ipv0,\
             'ipv1': goodweSample.goodweSample.get_ipv1,\
             'vac0': goodweSample.goodweSample.get_vac0,\
             'vac1': goodweSample.goodweSample.get_vac1,\
             'vac2': goodweSample.goodweSample.get_vac2,\
             'iac0': goodweSample.goodweSample.get_iac0,\
             'iac1': goodweSample.goodweSample.get_iac1,\
             'iac2': goodweSample.goodweSample.get_iac2,\
             'fac0': goodweSample.goodweSample.get_fac0,\
             'fac1': goodweSample.goodweSample.get_fac1,\
             'fac2': goodweSample.goodweSample.get_fac2,\
             'pgrid': goodweSample.goodweSample.get_pgrid,\
             'eday': goodweSample.goodweSample.get_eday,\
             'etotal': goodweSample.goodweSample.get_etotal,\
             'htotal': goodweSample.goodweSample.get_htotal,\
             'temperature': goodweSample.goodweSample.get_temperature,\
             'efficiency': goodweSample.goodweSample.get_efficiency }

   #--------------------------------------------------------------------------
   def __init__( self, pvoutput):
   # Processing class. This class converts the data from the Goodwe logging
   # frequency of once every 10 min, to the log interval of 5 min of PVoutput
   # by interpolating.
   #
      self.sampleBuffer = []
      self.log = None
      self.bufferedSamples = 0
      self.m_pvoutput = pvoutput

   #--------------------------------------------------------------------------
   def _fitSample(self, getter):
   #
      val = np.array([ getter(self.sampleBuffer[0]),\
                       getter(self.sampleBuffer[1]),\
                       getter(self.sampleBuffer[2]),\
                       getter(self.sampleBuffer[3]),\
                       getter(self.sampleBuffer[4])])
      y = np.array([ 0.0, 1.0, 2.0, 3.0, 4.0])
      z = np.polyfit( y, val, 2.0)
      
      p = np.poly1d(z)
      
      retval = p(3)
      
      if retval < 0.0:
         retval = 0.0
      return retval
      

            
   #--------------------------------------------------------------------------
   def fitAndLog( self, sample):
   #
      self.log = copy.deepcopy(sample)
      
      self.log.set_vpv(0, self._fitSample( self.funcs['vpv0']))
      self.log.set_vpv(1, self._fitSample( self.funcs['vpv1']))
      self.log.set_ipv(0, self._fitSample( self.funcs['ipv0']))
      self.log.set_ipv(1, self._fitSample( self.funcs['ipv1']))
      self.log.set_vac(0, self._fitSample( self.funcs['vac0']))
      self.log.set_vac(1, self._fitSample( self.funcs['vac1']))
      self.log.set_vac(2, self._fitSample( self.funcs['vac2']))
      self.log.set_iac(0, self._fitSample( self.funcs['iac0']))
      self.log.set_iac(1, self._fitSample( self.funcs['iac1']))
      self.log.set_iac(2, self._fitSample( self.funcs['iac2']))
      self.log.set_fac(0, self._fitSample( self.funcs['fac0']))
      self.log.set_fac(1, self._fitSample( self.funcs['fac1']))
      self.log.set_fac(2, self._fitSample( self.funcs['fac2']))
      self.log.set_pgrid( self._fitSample( self.funcs['pgrid']))
      self.log.set_eday( self._fitSample( self.funcs['eday']))
#      self.log.set_etotal( self._fitSample( self.funcs['etotal']))
#      self.log.set_htotal( self._fitSample( self.funcs['htotal']))
      self.log.set_temperature( self._fitSample( self.funcs['temperature']))
      self.log.set_efficiency( self._fitSample( self.funcs['efficiency']))
      
      if self.m_pvoutput:
         self.m_pvoutput.post_data( self.log)
      t = time.localtime(time.time())
      print "Logging:  " + str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2) + "h " + self.log.to_short_string()

   
   #--------------------------------------------------------------------------
   def processSample( self, sample):
   #
      if (self.bufferedSamples < 5):
         self.sampleBuffer.append( sample);
         self.bufferedSamples += 1
         t = time.localtime(time.time())
         print "Buffering: " + str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2) + "h " + sample.to_short_string()
      else:
         self.fitAndLog( self.sampleBuffer[2])
         self.sampleBuffer[0] = self.sampleBuffer[1]
         self.sampleBuffer[1] = self.sampleBuffer[2]
         self.sampleBuffer[2] = self.sampleBuffer[3]
         self.sampleBuffer[3] = self.sampleBuffer[4]
         self.sampleBuffer[4] = sample
      

   #--------------------------------------------------------------------------
   def getSample( self, getter):
   #
      return self.funcs[getter](self.log)


   #--------------------------------------------------------------------------
   def reset( self):
   # Resets the processing class when the inverter goes offline and logs the
   # last sample.
   #
      self.sampleBuffer = []
      self.bufferedSamples = 0
      self.log = None
   

#---------------- End of file ------------------------------------------------
