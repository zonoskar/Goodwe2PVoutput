class goodweConfig :
   GOODWE_SYSTEM_ID = 'goodwe_system_id'
   GOODWE_USER_ID = 'goodwe_user_id'
   GOODWE_PASSWD = 'goodwe_passwd'
   GOODWE_SERVER = 'goodwe_server'
   PVOUTPUT_SYSTEM_ID = 'pvoutput_system_id'
   PVOUTPUT_API = 'pvoutput_api'
   CSV_DIR = 'csv_dir'
   SPLINE_FIT = 'spline_fit'
   INPUT_SOURCE = 'input_source'
   SERIAL_BAUDRATE = 'serial_baudrate'
   SERIAL_DEVICE = 'serial_device'
   WIFI_ADDRESS = 'wifi_address'
   GPIO_USB_PIN = 'gpio_usb_pin'
   TEMP_MONITOR = 'temp_monitor'
   GPIO_FAN_V1 = 'gpio_fan_V1'
   GPIO_FAN_V2 = 'gpio_fan_V2'
   GPIO_FAN_ON1 = 'gpio_fan_on1'
   GPIO_FAN_ON2 = 'gpio_fan_on2'
   USB_SAMPLE_INTERVAL = 'usb_sample_interval'

   #--------------------------------------------------------------------------
   def __init__( self, configFile):
   # Initialization of the goodweConfig class. This class read the config
   # file and stores these.

      # These URLs should be okay for Goodwe-power and PVoutput.org (and yes,
      # there is a spelling error in the goodwe URL).
      self.pvoutput_url = 'http://pvoutput.org/service/r2/addstatus.jsp'
      self.spline_fit = False
      self.temp_monitor = False
      self.goodwe_passwd = ''
      
      with open( configFile) as fp:
         for line in fp:
            line = line[:line.find('#')]
            line = line.replace(' ', '')
            line = line.replace('=', '')
            line = line.replace(':\\', ';')
            line = line.replace(':', '')
            line = line.replace('\'', '')
            line = line.replace(';', ':\\')
            
            if self.GOODWE_SYSTEM_ID in line:
               self.goodwe_system_id = line.replace(self.GOODWE_SYSTEM_ID, '')
            if self.GOODWE_USER_ID in line:
               self.goodwe_user_id = line.replace(self.GOODWE_USER_ID, '')
            if self.GOODWE_PASSWD in line:
               self.goodwe_passwd = line.replace(self.GOODWE_PASSWD, '')
            if self.GOODWE_SERVER in line:
               self.goodwe_server = line.replace(self.GOODWE_SERVER, '')
            if self.PVOUTPUT_SYSTEM_ID in line:
               self.pvoutput_system_id = line.replace(self.PVOUTPUT_SYSTEM_ID, '')
            if self.PVOUTPUT_API in line:
               self.pvoutput_api = line.replace(self.PVOUTPUT_API, '')
            if self.CSV_DIR in line:
               self.csv_dir = line.replace(self.CSV_DIR, '')
            if self.SPLINE_FIT in line:
               self.spline_fit = line.replace(self.SPLINE_FIT, '') == "True"
            if self.INPUT_SOURCE in line:
               self.input_source = line.replace(self.INPUT_SOURCE, '')
            if self.SERIAL_BAUDRATE in line:
               self.serial_baudrate = line.replace(self.SERIAL_BAUDRATE, '')
            if self.SERIAL_DEVICE in line:
               self.serial_device = line.replace(self.SERIAL_DEVICE, '')
            if self.WIFI_ADDRESS in line:
               self.wifi_address = line.replace(self.WIFI_ADDRESS, '')
            if self.GPIO_USB_PIN in line:
               self.gpio_usb_pin = line.replace(self.GPIO_USB_PIN, '')
            if self.GPIO_FAN_V1 in line:
               self.gpio_fan_V1 = line.replace(self.GPIO_FAN_V1, '')
            if self.TEMP_MONITOR in line:
               self.temp_monitor = line.replace(self.TEMP_MONITOR, '') == "True"
            if self.GPIO_FAN_V2 in line:
               self.gpio_fan_V2 = line.replace(self.GPIO_FAN_V2, '')
            if self.GPIO_FAN_ON1 in line:
               self.gpio_fan_on1 = line.replace(self.GPIO_FAN_ON1, '')
            if self.GPIO_FAN_ON2 in line:
               self.gpio_fan_on2 = line.replace(self.GPIO_FAN_ON2, '')
            if self.USB_SAMPLE_INTERVAL in line:
               self.usb_sample_interval = float(line.replace(self.USB_SAMPLE_INTERVAL, ''))


#OLD      self.goodwe_url = 'http://%s.goodwe-power.com/PowerStationPlatform/PowerStationReport/InventerDetail' % (self.goodwe_server)
#         self.goodwe_loginUrl = 'http://%s.goodwe-power.com/User/Login' % (self.goodwe_server)
      self.goodwe_url = 'https://www.semsportal.com'
      self.goodwe_loginUrl = '/home/login'

   #--------------------------------------------------------------------------
   def to_string( self):
   # Prints a string representation fo the class
   #
      print "Goodwe URL: (" + self.goodwe_url + ")"
      print "Goodwe Login URL: (" + self.goodwe_loginUrl + ")"
      print self.GOODWE_SYSTEM_ID + " (" + self.goodwe_system_id + ")"
      print self.GOODWE_USER_ID + " (" + self.goodwe_user_id + ")"  
      if self.goodwe_passwd == '':
         print "Ask for Goodwe-power password"
      else:
         print "Goodwe-power password supplied"
      print "PVOutput upload URL: (" + self.pvoutput_url + ")"
      print self.PVOUTPUT_SYSTEM_ID + " (" + self.pvoutput_system_id + ")"
      print self.PVOUTPUT_API + " (" + self.pvoutput_api + ")"
      print self.CSV_DIR + " (" + self.csv_dir + ")"
      print self.SPLINE_FIT + " (" + str(self.spline_fit) + ")"
      print self.INPUT_SOURCE + " (" + str(self.input_source) + ")"
      
      try:
         print self.SERIAL_BAUDRATE + " (" + str(self.serial_baudrate) + ")"
         print self.SERIAL_DEVICE + " (" + str(self.serial_device) + ")"
         print self.WIFI_ADDRESS + " (" + str(self.wifi_address) + ")"
         print self.GPIO_USB_PIN + " (" + str(self.gpio_usb_pin) + ")"
         print self.USB_SAMPLE_INTERVAL + " (" + str(self.usb_sample_interval) + ")"
         print self.TEMP_MONITOR + " (" + str(self.temp_monitor) + ")"
         print "FAN pins: (" + str(self.gpio_fan_V1) + ", " + str(self.gpio_fan_V2) + ", " + str(self.gpio_fan_on1) + ", " + str(self.gpio_fan_on2) + ")"
      except:
         pass
            
   #--------------------------------------------------------------------------
   def get_goodwe_system_id( self):
   # Returns the goodwe_system_id
   #
      return self.goodwe_system_id

   #--------------------------------------------------------------------------
   def get_goodwe_user_id( self):
   # Returns the goodwe_user_id
   #
      return self.goodwe_user_id

   #--------------------------------------------------------------------------
   def get_goodwe_passwd( self):
   # Returns the goodwe_passwd
   #
      return self.goodwe_passwd

   #--------------------------------------------------------------------------
   def get_goodwe_server( self):
   # Returns the goodwe_server
   #
      return self.goodwe_server

   #--------------------------------------------------------------------------
   def get_pvoutput_system_id( self):
   # Returns the pvoutput_system_id
   #
      return self.pvoutput_system_id

   #--------------------------------------------------------------------------
   def get_pvoutput_api( self):
   # Returns the pvoutput_api
   #
      return self.pvoutput_api

   #--------------------------------------------------------------------------
   def get_csv_dir( self):
   # Returns the csv_dir
   #
      return self.csv_dir

   #--------------------------------------------------------------------------
   def get_goodwe_url( self):
   # Returns the goodwe_url
   #
      return self.goodwe_url

   #--------------------------------------------------------------------------
   def get_goodwe_loginUrl( self):
   # Returns the goodwe_loginUrl
   #
      return self.goodwe_loginUrl

   #--------------------------------------------------------------------------
   def get_pvoutput_url( self):
   # Returns the pvoutput_url
   #
      return self.pvoutput_url

   #--------------------------------------------------------------------------
   def get_spline_fit( self):
   # Returns the pvoutput_url
   #
      return self.spline_fit

   #--------------------------------------------------------------------------
   def get_input_source( self):
   # Returns the input_source
   #
      return self.input_source

   #--------------------------------------------------------------------------
   def get_serial_baudrate( self):
   # Returns the serial_baudrate
   #
      return self.serial_baudrate

   #--------------------------------------------------------------------------
   def get_serial_device( self):
   # Returns the serial_device
   #
      return self.serial_device

   #--------------------------------------------------------------------------
   def get_wifi_address( self):
   # Returns the wifi_address
   #
      return self.wifi_address

   #--------------------------------------------------------------------------
   def get_gpio_usb_pin( self):
   # Returns the USB GPIO pin
   #
      return self.gpio_usb_pin

   #--------------------------------------------------------------------------
   def get_temp_monitor( self):
   # Returns the FAN gpio pins
   #
      return self.temp_monitor

   #--------------------------------------------------------------------------
   def get_gpio_fan_pins( self):
   # Returns the FAN gpio pins
   #
      return (self.gpio_fan_V1, self.gpio_fan_V2, self.gpio_fan_on1, self.gpio_fan_on2)

   #--------------------------------------------------------------------------
   def get_usb_sample_interval( self):
   # Returns the USB sample period
   #
      return self.usb_sample_interval

#---------------- End of file ------------------------------------------------
