import usb
import array
import copy
import time
import zlib
import enum

import goodweSample
import iGoodwe


class CC:
   reg  = 0x00
   read = 0x01

class FC:
   # Register function codes
   offline    = 0x00
   allocreg   = 0x01
   query      = 0x01
   remreg     = 0x02
   query_id   = 0x02
   query_stt  = 0x03
   # Read function codes
   regreq     = 0x80
   result     = 0x81
   addconf    = 0x81
   result_id  = 0x82
   remconf    = 0x82
   result_stt = 0x83



class testUsb :

   #--------------------------------------------------------------------------
   def __init__(self, vendorId):
      '''Initialisation of the goodweUsb class. All data members are set
         to default values. '''
      self.m_serialNumber = ""
      self.m_sendBuffer = ''
      self.m_inverter_adr = 0x11
      self.m_inverter_adr_confirmed = False
      self.vendorId = vendorId

      self.cc_reg_switch  = {FC.offline:      self._reply_offline,
                             FC.regreq:       self._reply_regreq,
                             FC.allocreg:     self._reply_allocreg,
                             FC.addconf:      self._reply_addconf,
                             FC.remreg:       self._reply_remreg,
                             FC.remconf:      self._reply_remconf}

      self.cc_read_switch = {FC.query:        self._skip_message,
                             FC.result:       self._reply_read_data,
                             FC.query_id:     self._skip_message,
                             FC.result_id:    self._skip_message,
                             FC.query_stt:    self._skip_message,
                             FC.result_stt:   self._skip_message}


   def reset( self):
      pass
      
   def is_kernel_driver_active( self, level):
      return level == 0

   def detach_kernel_driver( self, level):
      pass

   def set_configuration( self):
      pass

   def get_active_configuration( self):
      return (0, 0, 1, 1, 2, 2)

   def read( self, epi, nr_bytes, timeout):
      buf = self.m_sendBuffer[0:nr_bytes]
      self.m_sendBuffer=self.m_sendBuffer[nr_bytes:]
      print "reading " + str(nr_bytes) + " bytes."
      time.sleep(1)
      return buf

   def ctrl_transfer( self, address, function, test1, test2, inBuffer):
      print "ctrl_transfer"
      hB = inBuffer[len(inBuffer)-2]
      lB = inBuffer[len(inBuffer)-1]
      hC,lC = self._calc_crc16( inBuffer[3:], len(inBuffer)-5)

      if not ((ord(hB) == hC) and (ord(lB) == lC)):
         raise ValueError("Calculated CRC doesn't match message CRC")

#     [0xCC, 0x99, len(buf)]) + [0xAA, 0x55, 0x80, address, cc, fc]) + data

      lenn =  ord(inBuffer[2])
      if ord(inBuffer[2]) != len(inBuffer)-3:
         raise ValueError("Buffer length does not match")
      
      src = ord(inBuffer[5])
      adr = ord(inBuffer[6])
      cc =  ord(inBuffer[7])
      fc =  ord(inBuffer[8])
      data =  inBuffer[9:]

      # Call the reply function for the received message
      if cc == CC.reg:
         print "Registration"
         self.cc_reg_switch[fc]( src, lenn, inBuffer)
      elif cc == CC.read:
         print "Read"
         self.cc_read_switch[fc]( src, lenn, inBuffer)
      return len(inBuffer)


   def _reply_offline( self, src, lenn, inBuffer):
      print "_reply_offline"
      
   def _reply_regreq( self, src, lenn, inBuffer):
      print "_reply_regreq"
      
   def _reply_allocreg( self, src, lenn, inBuffer):
      print "_reply_allocreg"
      
   def _reply_addconf( self, src, lenn, inBuffer):
      print "_reply_addconf"
      
   def _reply_remreg( self, src, lenn, inBuffer):
      print "_reply_remreg"
      self.m_sendBuffer=''.join(chr(x) for x in [0xAA,0x55,0x00,0x80, 0x00,0x01,0x5,0x1,0x2,0x3,0x4,0x5])
      h,l = self._calc_crc16( self.m_sendBuffer, len(self.m_sendBuffer))
      self.m_sendBuffer+=''.join(chr(x) for x in [h,l])
      
   def _reply_remconf( self, src, lenn, inBuffer):
      print "_reply_remconf"
      

   def _skip_message( self, src, lenn, inBuffer):
      print "_skip_message"
      
   def _reply_read_data( self, src, lenn, inBuffer):
      print "_reply_read_data"
      

   #--------------------------------------------------------------------------
   def _calc_crc16( self, buf, length):
      '''Calculate the CRC from the message.'''
      crc = 0
      for cnt in xrange(length):
         crc += ord(buf[cnt])

      #write out the high and low
      high = (crc >> 8) & 0xff;
      low = crc & 0xff;

      return high, low





#---------------- End of file ------------------------------------------------
