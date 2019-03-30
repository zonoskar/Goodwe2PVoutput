import goodweConfig
import goodweData

class GoodweFactory :
   #--------------------------------------------------------------------------
   def __init__( self, config):
      self.config = config
      
   #--------------------------------------------------------------------------
   def create( self, pvoutput):
      '''Create a goodwe instance.'''
      goodwe = None
      process = None
      
      if self.config.get_input_source() == 'USB':
         import goodweUsb
         import processNone
         goodwe = goodweUsb.goodweUsb( self.config.get_gpio_usb_pin(), 
                                       self.config.get_usb_sample_interval(), 
                                       0x0084)
         process = processNone.processNone( pvoutput)

      elif self.config.get_input_source() == 'RS485':
         import goodweRS485
         import processNone
         goodwe = goodweRS485.goodweRS485( '', 
                                           self.config.get_serial_device(), 
                                           self.config.get_serial_baudrate())
         process = processNone.processNone( pvoutput)

      elif self.config.get_input_source() == 'WIFI':
         import goodweWIFI
         import processNone
         goodwe = goodweWIFI.goodweWIFI(   self.config.get_wifi_address(), 
                                           '', 
                                           self.config.get_serial_baudrate())
         process = processNone.processNone( pvoutput)

      else: # self.config.get_input_source() == 'URL':
         import readGoodwe
         goodwe = readGoodwe.readGoodwe( self.config.get_goodwe_url(), 
                                         self.config.get_goodwe_loginUrl(), 
                                         self.config.get_goodwe_system_id())
         # Request password for Goodwe-power.com
         password = self.config.get_goodwe_passwd()
         if password == '':
            passwd_text = 'Supply password for ' + str(self.config.get_goodwe_loginUrl()) + ': '
            password = getpass.getpass( passwd_text)
         goodwe.login( self.config.get_goodwe_user_id(), password)

         if self.config.get_spline_fit():
            import processData2
            process = processData2.processData2( pvoutput)
         else:
            import processData
            process = processData.processData( pvoutput)

      return goodwe, process
                     
#---------------- End of file ------------------------------------------------
