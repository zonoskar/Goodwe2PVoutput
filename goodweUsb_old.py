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
        
      self.init_message =''.join(chr(x) for x in [0xAA,0x55,0x80,0x7F,0x00,0x00,0x00])
      self.init_reply   =''.join(chr(x) for x in [0xAA,0x55,0x7F,0x80,0x00,0x80,0x10])
      self.rem_message  =''.join(chr(x) for x in [0xAA,0x55,0x80,0x0B,0x00,0x02,0x00])
      self.ack_message  =''.join(chr(x) for x in [0xAA,0x55,0x80,0x7F,0x00,0x01,0x11])
      self.ack_reply    =''.join(chr(x) for x in [0xAA,0x55,0x80,0x7F,0x00,0x01,0x11])
      self.data_message =''.join(chr(x) for x in [0xAA,0x55,0x80,0x11,0x01,0x01,0x00])
      self.data_start   =''.join(chr(x) for x in [0xAA,0x55,0x11,0x80,0x01,0x81,0x00])

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
   def usb_init( self):
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
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_sample.is_inverter_status('Normal')) and (abs(self.m_sample.get_vpv(0)+self.m_sample.get_vpv(1)) > 0.01))
      

   #--------------------------------------------------------------------------
   def terminate_usb( self):
      '''This terminates the USB driver'''
      usb.util.dispose_resources( self.m_dev)
      self.m_dev = None
      self.m_epi = None
      #self.m_sample.set_online( 'Offline')
      self.m_initialized = False


   #--------------------------------------------------------------------------
   def _crc16( self, buffer):
      crc = 0
      for cnt in xrange(len(buffer)):
         crc += ord(buffer[cnt])
   
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
   def _create_send_buffer( self, buffer):
      '''This creates the send buffer'''
      if append:
         buffer=buffer+append
      # calculate the CRC of the buffer
      h,l=self._crc16(buffer)
      buffer=buffer + ''.join( [chr(h),chr(l)])

      sendBuffer=''.join( chr(x) for x in [0xCC, 0x99, len(buffer)])
#      sendBuffer=sendBuffer+buffer
#      self._hexprint("SendBuffer", sendBuffer)

      return sendBuffer+buffer


   #--------------------------------------------------------------------------
   def _goodwe_send( self, sendBuffer):
      lenn = self.m_dev.ctrl_transfer( 0x21, 0x09, 0, 0, sendBuffer)

      if lenn != len(sendBuffer):
         print 'received length ' + str(lenn) + ' is not ' + str(len(sendBuffer)) + '.'

      return lenn


   #--------------------------------------------------------------------------
   def _send_init_goodwe_msg( self):
      '''This initializes the Goodwe inverter'''
      sendBuffer=self._create_send_buffer( self.init_message)
      self._hexprint( "sendBuffer in send_init_goodwe_msg", sendBuffer)
      try:
         lenn = self._goodwe_send( sendBuffer)
      except Exception, ex:
         raise IOError( "Unable send init message: " + str(ex))

      try:
         received_buffer = self._goodwe_receive( 8*8)
         self._hexprint( "received buffer in send_init_goodwe_msg", received_buffer)
      except Exception, ex:
         raise IOError( "Unable to init Goodwe USB: " + str(ex))

      # extract serial number
      ss = received_buffer.find(self.init_reply) + len(self.init_reply)
      serial=received_buffer[ss:ss+16]
      serial=serial+chr(0x11)
      self._hexprint( "Received serial", serial)
      return serial


   #--------------------------------------------------------------------------
   def _hexprint( self, string, data):
      print string
      ret=':'
      for character in data:
        ret += '0x' + character.encode('hex') + ':'
      print ret


   #--------------------------------------------------------------------------
   def _send_ack_goodwe_msg( self, serial):
      '''This initializes the Goodwe inverter'''
      print "Sending Goodwe initialize ACK"
      sendBuffer=self._create_send_buffer( self.ack_message, serial)

      try:
         lenn = self._goodwe_send( sendBuffer)
      except Exception, ex:
         raise IOError( "Unable to send ACK message: " + str(ex))

      try:
         received_buffer = self._goodwe_receive( 8*8)
         self._hexprint( "Received buffer", received_buffer)
      except Exception, ex:
         raise IOError( "Unable to send Goodwe USB acknowledge: " + str(ex))

      ss = received_buffer.find(self.ack_reply) + len(self.ack_reply)
      
      return "".join(x.encode('ascii') for x in received_buffer[ss:ss+16])


   #--------------------------------------------------------------------------
   def _remove_goodwe( self):
      '''This removes the Goodwe inverter'''
      sendBuffer=self._create_send_buffer( self.rem_message)
      self._hexprint( "Remove goodwe", sendBuffer)
      try:
         lenn = self._goodwe_send( sendBuffer)
      except Exception, ex:
         raise IOError( "Unable to remove Goodwe inverter: " + str(ex))


   #--------------------------------------------------------------------------
   def _read_data_goodwe( self):
      more = True

      while more:
         try:
            lenn = self._goodwe_send( sendBuffer)
         except Exception, ex:
            raise IOError( "Unable to send read data message: " + str(ex))

         try:
            received = self._goodwe_receive( 9*8)
            self._hexprint( "Received data buffer from read", received)
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
   def read_sample_data( self):
      if not self.m_initialized:
         self.initialize()
      try:
         data = self._read_data_goodwe()
         self._convert_data( data)
         print self.m_sample.to_string()
      except Exception, ex:
         print "Error, set offline"
#	 self.m_sample.set_online( 'Offline')
         raise IOError( "Cannot read from GoodweUSB: " + str(ex))

      return self.m_sample


   #--------------------------------------------------------------------------
   def initialize( self):
      tries = 0
      self.m_initialized = False

      while not self.m_initialized:
         print "Try init " + str(tries)
         try:
            print "Init goodwe"
            self._remove_goodwe()
            serial = self._send_init_goodwe_msg()
            sn = self._send_ack_goodwe_msg( serial)
            print "All initialized"
         except Exception, ex:
            print "Received exception: \'" +str(ex)+ "\' Trying again."
#            self.terminate_usb()
#            time.sleep(3)
#            self.usb_init()
            time.sleep(2)
#            self._remove_goodwe()

            tries+=1
            if (tries > 40):
               raise IOError("Cannot initialize Goodwe inverter via USB: " + str(ex))
         else:
            self.m_sample.set_inverter_sn( sn)
            self.m_initialized = True


   #--------------------------------------------------------------------------
   def terminate( self):
      terminate_usb()


#---------------- End of file ------------------------------------------------
