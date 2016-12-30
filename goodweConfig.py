import logging

class goodweConfig :
   GOODWE_SYSTEM_ID = 'goodwe_system_id'
   GOODWE_USER_ID = 'goodwe_user_id'
   GOODWE_PASSWORD = 'goodwe_password'
   PVOUTPUT_SYSTEM_ID = 'pvoutput_system_id'
   PVOUTPUT_API = 'pvoutput_api'
   CSV_DIR = 'csv_dir'

   #--------------------------------------------------------------------------
   def __init__( self, configFile):
   # Initialization of the goodweConfig class. This class read the config
   # file and stores these.

      # These URLs should be okay for GoodWe-power and PVOutput.org (and yes,
      # there is a spelling error in the GoodWe URL).
      self.goodwe_url = 'http://goodwe-power.com/PowerStationPlatform/PowerStationReport/InventerDetail'
      self.goodwe_loginUrl = 'http://goodwe-power.com/User/Login'
      self.goodwe_password = None
      self.pvoutput_url = 'http://pvoutput.org/service/r2/addstatus.jsp'

      with open( configFile) as fp:
         for line in fp:
            line = line[:line.find('#')]
            fields = line.split(":", 2)
            if len(fields) < 2:
               continue
            key = fields[0].strip()
            value = fields[1].strip()
            if value.startswith("'") and value.endswith("'"):
               value = value[1:-1]

            if self.GOODWE_SYSTEM_ID == key:
               self.goodwe_system_id = value
            if self.GOODWE_USER_ID == key:
               self.goodwe_user_id = value
            if self.GOODWE_PASSWORD == key:
               self.goodwe_password = value
            if self.PVOUTPUT_SYSTEM_ID == key:
               self.pvoutput_system_id = value
            if self.PVOUTPUT_API == key:
               self.pvoutput_api = value
            if self.CSV_DIR == key:
               self.csv_dir = value


   #--------------------------------------------------------------------------
   def to_string( self):
   # Prints a string representation fo the class
   #
      logging.debug("GoodWe login URL: " + self.goodwe_loginUrl)
      logging.debug("GoodWe status URL: " + self.goodwe_url)
      logging.debug("GoodWe system ID: " + self.goodwe_system_id)
      logging.debug(self.GOODWE_USER_ID + ": " + self.goodwe_user_id)
      if self.goodwe_password is not None:
          logging.debug(self.GOODWE_PASSWORD + ": ********")
      logging.debug("PVOutput upload URL: " + self.pvoutput_url)
      logging.debug(self.PVOUTPUT_SYSTEM_ID + ": " + self.pvoutput_system_id)
      logging.debug(self.PVOUTPUT_API + ": " + self.pvoutput_api)
      logging.debug(self.CSV_DIR + ": " + self.csv_dir)


   #--------------------------------------------------------------------------
   def get_goodwe_system_id( self):
   # Returns the goodwe_system_id
   #
      return self.goodwe_system_id


   #--------------------------------------------------------------------------
   def get_goodwe_password( self):
   # Returns the goodwe_password
   #
      return self.goodwe_password


   #--------------------------------------------------------------------------
   def get_goodwe_user_id( self):
   # Returns the goodwe_user_id
   #
      return self.goodwe_user_id


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
