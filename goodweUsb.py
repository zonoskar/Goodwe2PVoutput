import usb
import array
import copy
import time
import zlib

import goodweSample
import iGoodwe
  
class goodweUsb( iGoodwe.iGoodwe) :

   #--------------------------------------------------------------------------
   def __init__( self, deviceId):
   #Initialisation of the goodweUsb class. All data members are set
   #to default values. 
      self.m_sample = goodweSample.goodweSample()
      self.m_received_buffer=''
      self.m_received_last_pos=0
      self.m_dev = None
      self.m_epi = None
      self.m_initialized = False
      self.m_deviceId = deviceId
        
      self.init_message =''.join(chr(x) for x in [0xCC,0x99,0x09,0xAA,0x55,0x80,0x7F,0x00,
                                                  0x00,0x00,0x01,0xFE,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

      self.init_reply   =''.join(chr(x) for x in [0xAA,0x55,0x7F,0x80,0x00,0x80,0x10])

      self.ack_message  =''.join(chr(x) for x in [0xCC,0x99,0x1A,0xAA,0x55,0x80,0x7F,0x00, 
                                                  0x01,0x11,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

      self.ack_reply    =''.join(chr(x) for x in [0xAA,0x55,0x80,0x7F,0x00,0x01,0x11])

      self.data_message =''.join(chr(x) for x in [0xCC,0x99,0x09,0xAA,0x55,0x80,0x11,0x01, 
                                                  0x01,0x00,0x01,0x92,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                                  0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

      self.data_start   =''.join(chr(x) for x in [0x55,0x11,0x80,0x01,0x81])


   #--------------------------------------------------------------------------
   def usb_init( self):
      '''This initialises the USB device'''
      self.m_dev = usb.core.find(idVendor = self.m_deviceId)
      self.m_dev.reset()
   
      if self.m_dev is None:
         raise ValueError('Device for vendor GoodWe (vendor ID %s) not found' % str(vendor))
   
      if self.m_dev.is_kernel_driver_active(0) is True:
         print "but we need to detach kernel driver."
         self.m_dev.detach_kernel_driver(0)
         print "claiming device."
   
      try:
         print "Setting default USB configuration."
         self.m_dev.set_configuration()
      except:
         raise ValueError('Error setting USB configuration')
   
      try:
         print "Claiming USB interface."
         usb.util.claim_interface( self.m_dev, 0)
      except:
         raise ValueError('Error claiming USB interface')
   
      print "Getting active USB configuration."
      cfg = self.m_dev.get_active_configuration()
   
      intf = cfg[(0, 0)]
   
      # get the BULK IN descriptor
      self.m_epi = usb.util.find_descriptor(
         intf,
         # match our first out endpoint
         custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN) 


   #--------------------------------------------------------------------------
   def terminate_usb( self):
      '''This terminates the USB driver'''
      usb.util.dispose_resources( self.m_dev)
      self.m_dev = None
      self.m_epi = None
      self.m_sample.set_online( 'Offline')
      self.m_initialized = False


   #--------------------------------------------------------------------------
   def _crc16( self, buffer, dataLength):
      crc = 0
      for cnt in xrange(dataLength-3):
         crc += ord(buffer[cnt+3])
   
      #write out the high and low
      high = (crc >> 8) & 0xff;
      low = crc & 0xff;
   
      return high, low


   #--------------------------------------------------------------------------
   def _update_message( self, message, insert, pos):
      buf=list(message)

      for p,c in enumerate(insert):
         buf[p+pos] = c
      buffer=''.join(buf)

      return buffer


   #--------------------------------------------------------------------------
   def _assemble_buffer( self, buffer):
      incomplete=False
      ss=buffer.find(self.data_start)
      se=buffer.find(self.data_start, ss+1, len(buffer))

      if ss != -1:
         if self.m_received_last_pos == 0:
            if se == -1:
               self.m_received_buffer=buffer[ss:]
               self.m_received_last_pos = len(self.m_received_buffer)
               incomplete = True
            else:
               self.m_received_buffer=buffer[ss:se]
         else:
            self.m_received_buffer += buffer[:ss]
      else:
         if self.m_received_last_pos != 0:
            self.m_received_buffer += buffer
            self.m_received_last_pos = len(self.m_received_buffer)
         incomplete = True
   
      return incomplete


   #--------------------------------------------------------------------------
   def _goodwe_receive( self, num_bytes):
      '''This receives data from the Goodwe inverter'''
      receive = ''
      try:
         for loop in xrange(num_bytes/8):
            dat = self.m_dev.read( self.m_epi, 8, 1000)
            for d in dat:
               receive += chr(d)
      except Exception as ex:
         raise IOError( "Error reading: " + str(ex))

      return receive


   #--------------------------------------------------------------------------
   def _send_init_goodwe_msg( self):
      '''This initializes the Goodwe inverter'''

      lenn = self.m_dev.ctrl_transfer( 0x21, 0x09, 0, 0, self.init_message)
      if lenn != 72:
         print 'received length ' + str(lenn) + ' is not 72.'

      try:
         received_buffer = self._goodwe_receive( 8*8)
      except Exception, ex:
         raise IOError( "Unable to init Goodwe USB" + str(ex))

      # extract serial number
      ss = received_buffer.find(self.init_reply) + len(self.init_reply)

      return received_buffer[ss:ss+16]


   #--------------------------------------------------------------------------
   def _send_ack_goodwe_msg( self, serial):

      buffer=self._update_message( self.ack_message, serial, 10)
      crc=''.join(chr(x) for x in self._crc16(buffer, 28))
      buffer=self._update_message( buffer, crc, 27)

      try:
         lenn = self.m_dev.ctrl_transfer( 0x21, 0x09, 0, 0, buffer)
         received_buffer = self._goodwe_receive( 8*8)
      except Exception, ex:
         raise IOError( "Unable to send Goodwe USB acknowledge" + str(ex))

      ss = received_buffer.find(self.ack_reply) + len(self.ack_reply)
      
      return "".join(x.encode('ascii') for x in receive[ss:ss+16])


   #--------------------------------------------------------------------------
   def _read_data_goodwe( self):
      more = True

      while more:
         lenn = self.m_dev.ctrl_transfer( 0x21, 0x09, 0, 0, self.data_message)
#         print "Transferred " + str(lenn) + " bytes for read_data."
         try:
            received = self._goodwe_receive( 9*8)
         except Exception, ex:
            raise IOError( "Unable to read from Goodwe USB " + str(ex))
         else:
            more = self._assemble_buffer( received)
 
      return self.m_received_buffer


   #--------------------------------------------------------------------------
   def _scale_data( self, indata, offset, length, factor):
      res = 0.0
      for i in xrange(length):
         h = int(indata[offset+i].encode('hex'),16)
         res = res * 256.0 + float(h)

      return res / factor


   #--------------------------------------------------------------------------
   def _convert_data( self, indata):
      base = 6
      self.m_sample.set_vpv(0, self._scale_data( indata, base+ 0, 2,  10.0))
      self.m_sample.set_vpv(1, self._scale_data( indata, base+ 2, 2,  10.0))
      self.m_sample.set_ipv(0, self._scale_data( indata, base+ 4, 2,  10.0))
      self.m_sample.set_ipv(1, self._scale_data( indata, base+ 6, 2,  10.0))
      self.m_sample.set_vac(0, self._scale_data( indata, base+ 8, 2,  10.0))
      self.m_sample.set_vac(1, self._scale_data( indata, base+10, 2,  10.0))
      self.m_sample.set_vac(2, self._scale_data( indata, base+12, 2,  10.0))
      self.m_sample.set_iac(0, self._scale_data( indata, base+14, 2,  10.0))
      self.m_sample.set_iac(1, self._scale_data( indata, base+16, 2,  10.0))
      self.m_sample.set_iac(2, self._scale_data( indata, base+18, 2,  10.0))
      self.m_sample.set_fac(0, self._scale_data( indata, base+20, 2, 100.0))
      self.m_sample.set_fac(1, self._scale_data( indata, base+22, 2, 100.0))
      self.m_sample.set_fac(2, self._scale_data( indata, base+24, 2, 100.0))
      self.m_sample.set_pgrid( self._scale_data( indata, base+26, 2,   1.0))

      if self._scale_data( indata, base+28, 2,   1.0) > 0.0:
         self.m_sample.set_online( 'Normal')
      else:
         self.m_sample.set_online( 'Offline')

      self.m_sample.set_temperature( self._scale_data( indata, base+30, 2,  10.0))
      self.m_sample.set_etotal( self._scale_data( indata, base+36, 4,  10.0))
      self.m_sample.set_htotal( self._scale_data( indata, base+40, 4,   1.0))
      self.m_sample.set_eday(   self._scale_data( indata, base+64, 2,  10.0))
      self.m_sample.set_error( indata[base+73:base+77])
      try:
         self.m_sample.set_eff( self.m_sample.get_pgrid() / ((self.m_sample.get_vpv(0) * self.m_sample.get_ipv(0)) + (self.m_sample.get_vpv(1) * self.m_sample.get_ipv(1))))
      except:
         self.m_sample.set_eff( 0.0)

      #Values that I'm not using (or don't know what they are
      self.m_sample.set_consume_day(0.0)
      self.m_sample.set_consume_total(0.0)
      self.m_sample.set_vbattery(0.0)
      self.m_sample.set_ibattery(0.0)
      self.m_sample.set_soc(0.0)
      self.m_sample.set_load(0.0)
      self.m_sample.set_description('')


   #--------------------------------------------------------------------------
   def read_sample_data( self):
      try:
         data = self._read_data_goodwe()
         self._convert_data( data)
      except Exception, ex:
	 self.m_sample.set_online( 'Offline')
         raise IOError( "Cannot read from GoodweUSB" + str(ex))

      return self.m_sample


   #--------------------------------------------------------------------------
   def initialize( self):
      if not self.m_initialized:
         try:
            self.m_initialized = False
            serial = self._send_init_goodwe_msg()
            sn = self._send_ack_goodwe_msg( serial)
         except Exception, ex:
            raise IOError( "Cannot initialize Goodwe inverter")
         else:
            self.m_sample.set_inverter_sn( sn)
            self.m_initialized = True


   #--------------------------------------------------------------------------
   def terminate( self):
      terminate_usb()


#---------------- End of file ------------------------------------------------
