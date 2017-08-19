import numpy as np
import goodweData
import copy

class processData2 :

   funcs = { 'vpv0': goodweData.goodweData.get_vpv0,\
	     'vpv1': goodweData.goodweData.get_vpv1,\
	     'ipv0': goodweData.goodweData.get_ipv0,\
	     'ipv1': goodweData.goodweData.get_ipv1,\
	     'vac0': goodweData.goodweData.get_vac0,\
	     'vac1': goodweData.goodweData.get_vac1,\
	     'vac2': goodweData.goodweData.get_vac2,\
	     'iac0': goodweData.goodweData.get_iac0,\
	     'iac1': goodweData.goodweData.get_iac1,\
	     'iac2': goodweData.goodweData.get_iac2,\
	     'fac0': goodweData.goodweData.get_fac0,\
	     'fac1': goodweData.goodweData.get_fac1,\
	     'fac2': goodweData.goodweData.get_fac2,\
	     'pgrid': goodweData.goodweData.get_pgrid,\
	     'eday': goodweData.goodweData.get_eday,\
	     'etotal': goodweData.goodweData.get_etotal,\
	     'htotal': goodweData.goodweData.get_htotal,\
	     'temperature': goodweData.goodweData.get_temperature,\
	     'efficiency': goodweData.goodweData.get_efficiency }

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
   def fitAndLog( self, gw):
   #
      self.log = copy.deepcopy(gw)
      
      self.log.m_vpv[0] = self._fitSample( self.funcs['vpv0'])
      self.log.m_vpv[1] = self._fitSample( self.funcs['vpv1'])
      self.log.m_ipv[0] = self._fitSample( self.funcs['ipv0'])
      self.log.m_ipv[1] = self._fitSample( self.funcs['ipv1'])
      self.log.m_vac[0] = self._fitSample( self.funcs['vac0'])
      self.log.m_vac[1] = self._fitSample( self.funcs['vac1'])
      self.log.m_vac[2] = self._fitSample( self.funcs['vac2'])
      self.log.m_iac[0] = self._fitSample( self.funcs['iac0'])
      self.log.m_iac[1] = self._fitSample( self.funcs['iac1'])
      self.log.m_iac[2] = self._fitSample( self.funcs['iac2'])
      self.log.m_fac[0] = self._fitSample( self.funcs['fac0'])
      self.log.m_fac[1] = self._fitSample( self.funcs['fac1'])
      self.log.m_fac[2] = self._fitSample( self.funcs['fac2'])
      self.log.m_pgrid = self._fitSample( self.funcs['pgrid'])
      self.log.m_eday = self._fitSample( self.funcs['eday'])
#      self.log.m_etotal = self._fitSample( self.funcs['etotal'])
#      self.log.m_htotal = self._fitSample( self.funcs['htotal'])
      self.log.m_temperature = self._fitSample( self.funcs['temperature'])
      self.log.m_efficiency = self._fitSample( self.funcs['efficiency'])
      
      if self.m_pvoutput:
         self.m_pvoutput.post_data( self.log)
      print "Logging: " + self.log.to_short_string()

   
   #--------------------------------------------------------------------------
   def processSample( self, gw):
   #
      if (self.bufferedSamples < 5):
         self.sampleBuffer.append( gw);
	 self.bufferedSamples += 1
	 print "Buffering sample " + gw.to_short_string()
      else:
         self.fitAndLog( self.sampleBuffer[2])
         self.sampleBuffer[0] = self.sampleBuffer[1]
         self.sampleBuffer[1] = self.sampleBuffer[2]
         self.sampleBuffer[2] = self.sampleBuffer[3]
         self.sampleBuffer[3] = self.sampleBuffer[4]
         self.sampleBuffer[4] = gw
      

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
   

