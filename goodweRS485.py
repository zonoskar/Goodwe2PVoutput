import array
import copy
import time
import zlib
import enum
import serial
import serial.rs485
import binascii

import goodweSample
import iGoodwe


class State( enum.Enum):
   OFFLINE = 1
   CONNECTED = 2
   DISCOVER = 3
   ALLOC = 4
   ALLOC_CONF = 5
   ALLOC_ASK = 6
   RUNNING = 7

class CC:
   reg  = 0x00
   read = 0x01

class FC:
   # Register function codes
   offline    = 0x00
   allocreg   = 0x01
   remreg     = 0x02
   regreq     = 0x80
   addconf    = 0x81
   remconf    = 0x82

   # Read function codes
   query      = 0x01
   query_id   = 0x02
   query_stt  = 0x03
   result     = 0x81
   result_id  = 0x82
   result_stt = 0x83


class goodweRS485( iGoodwe.iGoodwe) :

   #--------------------------------------------------------------------------
   def __init__(self, url, device, baudrate):
      '''Initialisation of the goodweRS485 class. All data members are set
         to default values. '''
      self.m_sample = goodweSample.goodweSample()
      self.m_state = State.OFFLINE
      self.m_serialNumber = ""
      self.m_serialBuffer = ''
      self.m_inverter_adr = 0x11
      self.m_inverter_adr_confirmed = False
      self.m_serial = None
      self.m_initialized = False
      self.m_emulated = "test" in url
      self.m_baudrate = baudrate
      self.m_device = device


      self.cc_reg_switch  = {FC.offline:      self._skip_message,
                             FC.regreq:       self._reg_received_registration,
                             FC.allocreg:     self._skip_message,
                             FC.addconf:      self._reg_received_confirm_registration,
                             FC.remreg:       self._skip_message,
                             FC.remconf:      self._reg_received_confirm_removal}

      self.cc_read_switch = {FC.query:        self._skip_message,
                             FC.result:       self._read_received_message,
                             FC.query_id:     self._skip_message,
                             FC.result_id:    self._skip_message,
                             FC.query_stt:    self._skip_message,
                             FC.result_stt:   self._skip_message}

      self.state_switch = { State.OFFLINE:    self.initialize,
			    State.CONNECTED:  self._remove_registration,
			    State.DISCOVER:   self._discover_goodwe,
			    State.ALLOC:      self._alloc_register,
			    State.ALLOC_CONF: self._read_data_goodwe,
			    State.ALLOC_ASK:  self._read_data_init,
			    State.RUNNING:    self._read_data }


   #--------------------------------------------------------------------------
   def initialize( self):
      '''Initialize the RS485 port'''
      tries = 0
      self.m_initialized = False
      self.m_state = State.OFFLINE

      try:
         self._rs485_init()
      except Exception, ex:
         raise IOError("Cannot initialize RS485 port: " + str(ex))
      else:
         self.m_initialized = True
         self.m_state = State.CONNECTED

      return False


   #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_sample.is_inverter_status('Normal')) and (abs(self.m_sample.get_vpv(0)+self.m_sample.get_vpv(1)) > 0.01))


   #--------------------------------------------------------------------------
   def read_sample_data( self):
      '''Read a data sample.'''
      print "Read sample data. State=" + str(self.m_state)
      tries = 0
      sample_read = False
      while not sample_read:
         try:
            expectAnswer = self.state_switch[self.m_state]()
            if expectAnswer:
               sample_read = self._read_data_goodwe()
         except Exception, ex:
            print "Exception found: " +str(ex)
            if tries < 10:
               self.m_state = State.CONNECTED
               tries+=1
            else:
               raise IOError( "Cannot read from GoodweRS485 in state %s: %s" % (str(self.m_state), str(ex)))

      return self.m_sample


   #--------------------------------------------------------------------------
   # internal functions
   #--------------------------------------------------------------------------
   def _rs485_init( self):
      '''This initialises the RS485 port'''
      self.m_serial = serial.Serial()
      self.m_serial.baudrate = self.m_baudrate
      self.m_serial.port = self.m_device
      self.m_serial.timeout = 1 # seconds
      self.m_serial.stopbits = serial.STOPBITS_ONE
      self.m_serial.bytesize = serial.EIGHTBITS
      self.m_serial.parity = serial.PARITY_NONE
      self.m_serial.rtscts = False
      self.m_serial.dsrdtr = False
      self.m_serial.xonxoff = False
#      self.m_serial.rs485_mode = serial.rs485.RS485Settings(True, False, False)
      
      time.sleep(1)
      self.m_serial.open()


   #--------------------------------------------------------------------------
   def _rs485_terminate( self):
      '''This terminates the RS485 port'''
      self.m_serial.close()
      time.sleep(2)
      self.m_serial = None
      self.m_initialized = False


   #--------------------------------------------------------------------------
   def _transmitMode( self):
      self.m_serial.setDTR(0)
      self.m_serial.setRTS(0)

   #--------------------------------------------------------------------------
   def _receiveMode( self):
      self.m_serial.setDTR(1)
      self.m_serial.setRTS(1)


   #--------------------------------------------------------------------------
   def _read_data_goodwe( self):
      '''Continiuously read messages from the Goodwe inverter until a complete
         message packet has been received. The start of the message is marked
         with 2 bytes: 0xAA, 0x55. The 5th byte represents the message length.'''
      sample_read = False
      more = True
      startFound = False
      dataLen = 0
      dataPtr = 0
      lastByte = 0x00
      inBuffer = ''

      self._receiveMode()
      try:
         while more:
            dataStream = self.m_serial.read(1)
            self._hexprint("RAW received:", dataStream)

            for byte in dataStream:
               if startFound:
                  if dataLen > 0 or dataPtr < 5:
                     inBuffer+=chr(byte)
                     dataPtr += 1
                     if dataPtr == 5:
                        dataLen = byte + 2
                     elif dataPtr > 5:
                        dataLen -= 1

                  if dataPtr >= 5 and dataLen == 0:
                     self._hexprint("inBuffer:", inBuffer)
                     startFound = False
                     sample_read = self._check_crc_and_update_state( inBuffer)
                     more = False

               if byte == 85 and lastByte == 170:
                  startFound = True
                  dataPtr = 0
                  dataLen = 0
                  inBuffer=''.join(chr(x) for x in [lastByte, byte])
                  lastByte = 0x00

               lastByte = byte
      except Exception, ex:
         print "Exception while read: " + str(ex) + ". Try again."
         pass

      return sample_read


   #--------------------------------------------------------------------------
   def _check_crc_and_update_state( self, inBuffer):
      '''Calculate the CRC from a message and compare to the sent CRC in the
         message from the Goodwe inverter, then interpret the received message 
         and call the correct message reply function. The CRC is encoded in the
         last 2 bytes and is not included in the CRC calculation.'''
      sample_read = False
      hB = inBuffer[len(inBuffer)-2]
      lB = inBuffer[len(inBuffer)-1]
      hC,lC = self._calc_crc16( inBuffer, len(inBuffer)-2)

      if not ((ord(hB) == hC) and (ord(lB) == lC)):
         raise ValueError("Calculated CRC (%s:%s) doesn't match message CRC (%s:%s)" %(hex(ord(hB)),hex(ord(lB)),hex(hC),hex(lC)))

      src = ord(inBuffer[2])
      dst = ord(inBuffer[3])
      cc =  ord(inBuffer[4])
      fc =  ord(inBuffer[5])
      lenn =ord(inBuffer[6])
      data = inBuffer[7:]

#      print "Src: " +str(src)
#      print "dst: " +str(dst)
#      print "cc: " +str(cc)
#      print "fc: " +str(fc)
#      print "lenn: " +str(lenn)
      # Call the reply function for the received message
      if cc == CC.reg:
         self.cc_reg_switch[fc]( src, lenn, data)
      elif cc == CC.read:
         sample_read = self.cc_read_switch[fc]( src, lenn, data)

      return sample_read


   #--------------------------------------------------------------------------
   def _calc_crc16( self, buffer, length):
      '''Calculate the CRC from the message.'''
      crc = 0
      for cnt in xrange(length):
         crc += ord(buffer[cnt])

      #return the high and low
      high = (crc >> 8) & 0xff;
      low = crc & 0xff;

      return high, low

   #--------------------------------------------------------------------------
   def _skip_message( self, src, lenn, inBuffer):
      '''Not all possible messages have been implemented/can be received. This
         handles those messages.'''
      print "An unused state was received: " + str(self.m_state) + "."

   #--------------------------------------------------------------------------
   def _reg_received_confirm_removal( self, src, lenn, inBuffer):
      '''When the inverter sends the removal confirm message.'''
      print "Inverter removed."
      self.m_serialBuffer = ''
      self.m_inverter_adr_confirmed = False

   #--------------------------------------------------------------------------
   def _reg_received_registration( self, src, lenn, inBuffer):
      '''When the inverter sends the registration message.'''
      print "Inverter registration received."
      self.m_serialBuffer = inBuffer[0:16]
      print "Serial number: " + str(self.m_serialBuffer)
      self.m_state = State.ALLOC

   #--------------------------------------------------------------------------
   def _reg_received_confirm_registration( self, src, lenn, inBuffer):
      '''When the inverter sends the registration confirmation message.'''
      print "Inverter registration confirmation received at address: " + hex(src)
      if self.m_inverter_adr == src:
         self.m_inverter_adr_confirmed = True
         self.m_state = State.ALLOC_ASK
      else:
         self.m_state = State.OFFLINE

   #--------------------------------------------------------------------------
   def _read_received_message( self, src, lenn, inBuffer):
      '''When the inverter sends the sample data.'''
      print "Read message received length: " + str(lenn)
      self._convert_data( inBuffer, lenn == 66)
      return True

   #--------------------------------------------------------------------------
   def _scale_data( self, indata, offset, length, factor):
      '''Function to decode and scale the received sample data.'''
      res = 0.0

      for i in xrange(length):
         h = int(indata[offset+i].encode('hex'),16)
         res = res * 256.0 + float(h)
      return res / factor

   #--------------------------------------------------------------------------
   def _convert_data( self, indata, isDTseries):
      '''Function to disassemble the incoming data into readable format.'''
      self.m_sample.set_inverter_sn( self.m_serialBuffer)
      self.m_sample.set_vpv(0, self._scale_data( indata, 0, 2,  10.0))
      self.m_sample.set_vpv(1, self._scale_data( indata, 2, 2,  10.0))
      self.m_sample.set_ipv(0, self._scale_data( indata, 4, 2,  10.0))
      self.m_sample.set_ipv(1, self._scale_data( indata, 6, 2,  10.0))
      self.m_sample.set_vac(0, self._scale_data( indata, 8, 2,  10.0))
      if isDTseries:
         self.m_sample.set_vac(1, self._scale_data( indata, 10, 2,  10.0))
         self.m_sample.set_vac(2, self._scale_data( indata, 12, 2,  10.0))
      self.m_sample.set_iac(0, self._scale_data( indata, 14, 2,  10.0))
      if isDTseries:
         self.m_sample.set_iac(1, self._scale_data( indata, 16, 2,  10.0))
         self.m_sample.set_iac(2, self._scale_data( indata, 18, 2,  10.0))
      self.m_sample.set_fac(0, self._scale_data( indata, 20, 2, 100.0))
      if isDTseries:
         self.m_sample.set_fac(1, self._scale_data( indata, 22, 2, 100.0))
         self.m_sample.set_fac(2, self._scale_data( indata, 24, 2, 100.0))
      self.m_sample.set_pgrid( self._scale_data( indata, 26, 2,   1.0))

      if self._scale_data( indata, 28, 2,   1.0) > 0.0:
         self.m_sample.set_inverter_status( 'Normal')
      else:
         self.m_sample.set_inverter_status( 'Offline')

      self.m_sample.set_temperature( self._scale_data( indata, 30, 2,  10.0))
      self.m_sample.set_etotal( self._scale_data( indata, 36, 4,  10.0))
      self.m_sample.set_htotal( self._scale_data( indata, 40, 4,   1.0))
      self.m_sample.set_eday(   self._scale_data( indata, 64, 2,  10.0))

      self.m_sample.set_error( indata[32:35])
      try:
         self.m_sample.set_efficiency( self.m_sample.get_pgrid() / ((self.m_sample.get_vpv(0) * self.m_sample.get_ipv(0)) + (self.m_sample.get_vpv(1) * self.m_sample.get_ipv(1))))
      except:
         self.m_sample.set_efficiency( 0.0)

      #Values that I'm not using (or don't know what they are
      self.m_sample.set_consume_day(0.0)
      self.m_sample.set_consume_total(0.0)
      self.m_sample.set_vbattery(0.0)
      self.m_sample.set_ibattery(0.0)
      self.m_sample.set_soc(0.0)
      self.m_sample.set_load(0.0)
      self.m_sample.set_description('Inverter address %s' % (hex(self.m_inverter_adr)))
#      print "So far: " + self.m_sample.to_detailed_string()


   #--------------------------------------------------------------------------
   def _remove_registration( self):
      '''Function to handle the message state machine. This function handles
         the removal of the registration state. No action is needed.'''
      print "Remove registration."
      self._goodwe_send( self.m_inverter_adr, CC.reg, FC.remreg, 0)
      self.m_state = State.DISCOVER
      time.sleep(1)
      return False

   #--------------------------------------------------------------------------
   def _discover_goodwe( self):
      '''Function to handle the message state machine. This function handles
         the discovery of the inverter. A message is sent.'''
      print "Discover Goodwe. address confirmed: " + str(self.m_inverter_adr_confirmed)
      if not self.m_inverter_adr_confirmed:
         self._goodwe_send( 0x7F, CC.reg, FC.offline, 0)
         return True
      return False


   #--------------------------------------------------------------------------
   def _alloc_register( self):
      '''Function to handle the message state machine. This function handles
         the registration of the inverter. A message is sent with the 
         previously received serial number.'''
      print "Allocating register for serial: " + str(self.m_serialBuffer)
      serial=self.m_serialBuffer
      print "Adding address"
      serial+=chr(self.m_inverter_adr)
      print "Allocated register for serial: " + str(self.m_serialBuffer) + " Sending..."

      self._goodwe_send( 0x7F, CC.reg, FC.allocreg, len(serial), serial)
      self.m_state = State.ALLOC_CONF
      return True

   #--------------------------------------------------------------------------
   def _no_action( self):
      '''Function to skip a certain state.'''
      print "An unused state was received: " + str(self.m_state) + "."
      return False

   #--------------------------------------------------------------------------
   def _read_data_init( self):
      '''Function to handle the message state machine. This function handles
         the first request of sample data. A message is sent with the
         previously negotiated inverter address.'''
      print "Reading data from Goodwe at address: " + hex(self.m_inverter_adr)
      self._goodwe_send( self.m_inverter_adr, CC.read, FC.query, 0)
      self.m_state = State.RUNNING
      return True

   #--------------------------------------------------------------------------
   def _read_data( self):
      '''Function to handle the message state machine. This function handles
         subsequent requests of sample data. A message is sent with the
         previously negotiated inverter address.'''
      print "Reading data from Goodwe at address: " + hex(self.m_inverter_adr)
      if self.m_inverter_adr_confirmed:
         self._goodwe_send( self.m_inverter_adr, CC.read, FC.query, 0)
	 return True
      else:
         raise IOError("Inverter not online, or address unkown. Cannot read.")

   #--------------------------------------------------------------------------
   def _goodwe_send( self, address, cc, fc, length, data = None):
#      print "Creating sendbuffer."
      sendBuffer=''.join(chr(x) for x in [0xAA, 0x55, 0x80, address, cc, fc, length])

      if data:
         sendBuffer+=data

      h,l = self._calc_crc16(sendBuffer, len(sendBuffer))
      sendBuffer+=''.join(chr(x) for x in [h,l])
      self._hexprint("goodwe send", sendBuffer)

      self._transmitMode()
      lenn = self.m_serial.write( sendBuffer)
      print "Write length: %d" % lenn
      if lenn != len(sendBuffer):
         print 'Write length ' + str(lenn) + ' is not ' + str(len(sendBuffer)) + '.'

      return lenn


   #--------------------------------------------------------------------------
   def _hexprint( self, string, data):
      ret=string + ':'
      for character in data:
        ret += '0x' + character.encode('hex') + ','
      print ret


   #--------------------------------------------------------------------------
   def terminate( self):
      self._rs485_terminate()


#---------------- End of file ------------------------------------------------
