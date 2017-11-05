import usb
import array
import copy
import time
import zlib

import goodweSample
import iGoodwe
  

class State( enum):
   OFFLINE = 1
   CONNECTED = 2
   DISCOVER = 3
   ALLOC = 4
   ALLOC_CONF = 5
   ALLOC_ASK = 6
   RUNNING = 7

class CC:
   # register function codes
   reg  = 0x00
   read = 0x01
   
class FC:
   offline    = 0x00
   allocreg   = 0x01
   query      = 0x01
   remreg     = 0x02
   query_id   = 0x02
   query_stt  = 0x03

   regreq     = 0x80
   result     = 0x81
   addconf    = 0x81
   result_id  = 0x82
   remconf    = 0x82
   result_stt = 0x83
   


class goodweUsb( iGoodwe.iGoodwe) :

   goodwe_adr = 0x80
   inverter_adr = 0x0b
   
   


   #--------------------------------------------------------------------------
   def __init__(self, url, login_url, station_id):
      '''Initialisation of the goodweUsb class. All data members are set
         to default values. '''
      self.m_sample = goodweSample.goodweSample()
      self.m_state = State.OFFLINE
      self.m_serialNumber = ""
      self.m_serialBuffer = ''
      self.m_inverter_adr = 0x11
      self.m_inverter_adr_confirmed = False

      self.cc_reg_switch  = {FC.offline:  self._skip_cc_message,
                             FC.regreq:   self._received_registration,
                             FC.allocreg: self._skip_cc_message,
                             FC.addconf:  self._received_confirm_registration,
                             FC.remreg:   self._skip_cc_message,
                             FC.remconf:  self._received_confirm_removal}
  
      self.cc_read_switch = {FC.query:      self._skip_cc_message,
                             FC.result:     self._read_received_message,
                             FC.query_id:   self._skip_cc_message,
                             FC.result_id:  self._skip_cc_message,
                             FC.query_stt:  self._skip_cc_message,
                             FC.result_stt: self._skip_cc_message}
  
      self.state_switch = { State.OFFLINE:    self.initialize,
			    State.CONNECTED:  self._remove_registration,
			    State.DISCOVER:   self._discover_goodwe,
			    State.ALLOC:      self._alloc_register,
			    State.ALLOC_CONF: self._no_action,
			    State.ALLOC_ASK:  self._read_data_init,
			    State.RUNNING:    self._read_data }
      
      
# Initialize message buffer
#      [0xCC,0x99,0x09,0xAA,0x55,0x80,0x7F,0x00,
#       0x00,0x00,0x01,0xFE,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

# Init Ack message buffer
#      [0xCC,0x99,0x1A,0xAA,0x55,0x80,0x7F,0x00, 
#       0x01,0x11,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x11,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

# Data message buffer
#      [0xCC,0x99,0x09,0xAA,0x55,0x80,0x11,0x01, 
#       0x01,0x00,0x01,0x92,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
#       0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])


   #--------------------------------------------------------------------------
   def initialize( self):
      '''Initialize the USB port'''
      tries = 0
      self.m_initialized = False

      while not self.m_initialized:
         try:
            self._terminate_usb()
            time.sleep(3)
            self._usb_init()

            tries+=1
            if (tries > 40):
               raise IOError("Cannot initialize USB port: " + str(ex))
         else:
            self.m_initialized = True


   #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_sample.is_inverter_status('Normal')) and (abs(self.m_sample.get_vpv(0)+self.m_sample.get_vpv(1)) > 0.01))

      
   #--------------------------------------------------------------------------
   def read_sample_data( self):
      '''Read a data sample.'''
      try:
         self.state_switch[self.m_state]()
      except Exception, ex:
         raise IOError( "Cannot read from GoodweUSB: " + str(ex))


   #--------------------------------------------------------------------------
   def _read_data( self):         
      try:
         data = self._read_data_goodwe()
         self._convert_data( data)
         print self.m_sample.to_string()
      except Exception, ex:
         print "Error, set offline"
#        self.m_sample.set_online( 'Offline')
         raise IOError( "Cannot read from GoodweUSB: " + str(ex))

      return self.m_sample
      
 
   #--------------------------------------------------------------------------
   # internal functions
   #--------------------------------------------------------------------------
   def _usb_init( self):
      '''This initialises the USB device'''
      self.m_dev = usb.core.find(idVendor = self.m_deviceId)
      self.m_dev.reset()
   
      if self.m_dev is None:
         raise ValueError('Device for vendor GoodWe (vendor ID %s) not found' % str(vendor))
   
      if self.m_dev.is_kernel_driver_active(0):
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
      print intf
   
      # get the BULK IN descriptor
      self.m_epi = usb.util.find_descriptor(
         intf,
         # match our first out endpoint
         custom_match= \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN) 


   #--------------------------------------------------------------------------
   def _terminate_usb( self):
      '''This terminates the USB driver'''
      usb.util.dispose_resources( self.m_dev)
      self.m_dev = None
      self.m_epi = None
      self.m_initialized = False


   #--------------------------------------------------------------------------
   def _read_data_goodwe( self):
      '''Read a message from the Goodwe inverter'''
      more = True
      startFound = False
      dataLen = 0
      dataPtr = 0
      lastByte = 0x00
      inBuffer = ''
      
      while more:
         try:
            dataStream = self.m_dev.read( self.m_epi, 8, 1000)
         except Exception, ex:
            raise IOError(" Unable to read 8 bytes from USB: " + str(ex)
            
         for byte in dataStream:
            if chr(byte) == 0x55 and lastByte == 0xAA:
               startFound = True
               dataPtr = 0
               dataLen = 0
               lastByte = 0x00
               inBuffer = chr(lastByte) + chr(byte)
         
            if startFound:
               if dataLen > 0 or self.dataPtr < 5:
                  inBuffer += chr(byte)
                  dataPtr += 1
                  if dataPtr == 5:
                     dataLen = ord(byte) + 2
                  elif dataPtr > 5:
                     dataLen -= 1
               if dataPtr >= 5 and dataLen = 0:
                  startFound = False
                  self._check_crc_and_update_state( inBuffer)
                  more = False
                   
            lastByte = byte
            
      return inBuffer


   #--------------------------------------------------------------------------
   def _check_crc_and_update_state( self, inBuffer):
      '''Read a message from the Goodwe inverter'''
      hB = inBuffer[len(inBuffer)-2]
      lB = inBuffer[len(inBuffer)-1]
      hC,lC = self._calc_crc16( inBuffer, len(inBuffer)-2)

      if not (hB == hC and lB == lC):
         raise ValueError("Calculated CRC doesn't match message CRC")
	 
      src = inBuffer[0]
      dst = inBuffer[1] 
      cc =  inBuffer[2]
      fc =  inBuffer[3]
      leng =  inBuffer[4]
      data =  inBuffer[5:]

      if cc == CC.reg:
         self.cc_reg_switch[fc]( src, leng, inBuffer)
      elif cc == CC.read:
         self.cc_read_switch[fc]( src, leng, inBuffer)


   #--------------------------------------------------------------------------
   def _calc_crc16( self, buffer, length):
      crc = 0
      for cnt in xrange(length)):
         crc += ord(buffer[cnt])
   
      #write out the high and low
      high = (crc >> 8) & 0xff;
      low = crc & 0xff;
   
      return high, low


   #--------------------------------------------------------------------------
   def _skip_cc_message( self, src, leng, inBuffer):
      print "An unused state was received: " + str(self.m_state) + "."
   
   #--------------------------------------------------------------------------
   def _received_confirm_removal( self, src, leng, inBuffer):
      print "Inverter removed."
      self.m_serialBuffer = ''
      self.m_inverter_adr_confirmed = False
   
   #--------------------------------------------------------------------------
   def _received_registration( self, src, leng, inBuffer):
      print "Inverter registration received."
      self.m_serialBuffer = inBuffer[0:16]
      self.m_state = State.ALLOC
      
   #--------------------------------------------------------------------------
   def _received_confirm_registration( self, src, leng, inBuffer):
      print "Inverter registration confirmation received."
      if self.m_inverter_adr == src:
         self.m_inverter_adr_confirmed = True

         self.m_state = State.ALLOC_ASK
      else:
         self.m_state = State.OFFLINE



   #--------------------------------------------------------------------------
   def _read_received_message( self, src, leng, inBuffer):
      self._convert_data( inBuffer, leng == 66)


   #--------------------------------------------------------------------------
   def _scale_data( self, indata, offset, length, factor):
      res = 0.0
      for i in xrange(length):
         h = int(indata[offset+i].encode('hex'),16)
         res = res * 256.0 + float(h)

      return res / factor


   #--------------------------------------------------------------------------
   def _convert_data( self, indata, isDTseries):
      base = 6
      self.m_sample.set_vpv(0, self._scale_data( indata, base+ 0, 2,  10.0))
      self.m_sample.set_vpv(1, self._scale_data( indata, base+ 2, 2,  10.0))
      self.m_sample.set_ipv(0, self._scale_data( indata, base+ 4, 2,  10.0))
      self.m_sample.set_ipv(1, self._scale_data( indata, base+ 6, 2,  10.0))
      self.m_sample.set_vac(0, self._scale_data( indata, base+ 8, 2,  10.0))
      if isDTseries:
         self.m_sample.set_vac(1, self._scale_data( indata, base+10, 2,  10.0))
         self.m_sample.set_vac(2, self._scale_data( indata, base+12, 2,  10.0))
      self.m_sample.set_iac(0, self._scale_data( indata, base+14, 2,  10.0))
      if isDTseries:
         self.m_sample.set_iac(1, self._scale_data( indata, base+16, 2,  10.0))
         self.m_sample.set_iac(2, self._scale_data( indata, base+18, 2,  10.0))
      self.m_sample.set_fac(0, self._scale_data( indata, base+20, 2, 100.0))
      if isDTseries:
         self.m_sample.set_fac(1, self._scale_data( indata, base+22, 2, 100.0))
         self.m_sample.set_fac(2, self._scale_data( indata, base+24, 2, 100.0))
      self.m_sample.set_pgrid( self._scale_data( indata, base+26, 2,   1.0))

      if self._scale_data( indata, base+28, 2,   1.0) > 0.0:
         #self.m_sample.set_online( 'Normal')
         print "Online"
      else:
         print "Offline"
         #self.m_sample.set_online( 'Offline')

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
   def _remove_registration( self):
   #--------------------------------------------------------------------------
   def _discover_goodwe( self):
      self._goodwe_send( 0x7F, CC.reg, FC.offline)
      
   #--------------------------------------------------------------------------
   def _alloc_register( self):
      serial=''.join(chr(x) for x in self.m_serialBuffer)
      serial+=self.m_inverter_adr
            
      self._goodwe_send( 0x7F, CC.reg, FC.allocreg, serial)
      self.m_state = State.ALLOC_CONF

   #--------------------------------------------------------------------------
   def _no_action( self):
      print "An unused state was received: " + str(self.m_state) + "."
      
   #--------------------------------------------------------------------------
   def _read_data_init( self):
      self._goodwe_send( self.m_inverter_adr, CC.read, FC.query)
      self.m_state = State.RUNNING

   #--------------------------------------------------------------------------
   def _read_data( self):
      self._goodwe_send( self.m_inverter_adr, CC.read, FC.query)


   #--------------------------------------------------------------------------
   def _goodwe_send( self, address, cc, fc, leng, data = None):
      sendBuffer=''.join([0xAA, 0x55, 0x80, address, cc, fc])
      if data:
         sendBuffer+=data
      h,l=self._calc_crc16(sendBuffer, len(sendBuffer))
      sendBuffer=sendBuffer + ''.join( [chr(h),chr(l)])
      sendBuffer=''.join( chr(x) for x in [0xCC, 0x99, len(sendBuffer)])
      self._hexprint("goodwe send", senfBuffer)
      
      lenn = self.m_dev.ctrl_transfer( 0x21, 0x09, 0, 0, sendBuffer)

      if lenn != len(sendBuffer):
         print 'received length ' + str(lenn) + ' is not ' + str(len(sendBuffer)) + '.'

      return lenn


   #--------------------------------------------------------------------------
   def _hexprint( self, string, data):
      ret=string + ':'
      for character in data:
        ret += '0x' + character.encode('hex') + ':'
      print ret


   #--------------------------------------------------------------------------
   def terminate( self):
      self._terminate_usb()


#---------------- End of file ------------------------------------------------
