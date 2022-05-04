import requests
import goodweData
import iGoodwe
import json

class readGoodwe( iGoodwe.iGoodwe) :

   #--------------------------------------------------------------------------
   def __init__(self, url, login_url, station_id):
   # Goodwe-power reading class. Reads the Goodwe-power.com website
   # from the specified URL and station ID.
   #
      self.subscribers= []
      self.m_goodwe_url = url
      self.m_goodwe_station_url = None
      self.m_login_url = url+login_url
      self.m_login_payload = None
      self.m_station_id = station_id
      self.m_session = None
      self.gwData = None
      

   #--------------------------------------------------------------------------
   def initialize( self):
      pass
      
   #--------------------------------------------------------------------------
   def subscribe_temperature( self, method):
   #Subscribes method to the temperature value.
   #
      self.subscribers.append( method)
   
   #--------------------------------------------------------------------------
   def login(self, username, password):
   # Log in Goodwe-power web site.
   #
      self.m_login_payload = {
         'account': username,
         'pwd': password }

      self.create_session()

   def create_session(self):
      url = self.m_login_url

      # Close old session
      if self.m_session:
         self.m_session.close()
         self.m_session = None

      # Start new session and authenticate
      with requests.Session() as self.m_session:
         print "Login URL: " + url
         p = self.m_session.post( url, data=self.m_login_payload)
         j=json.loads(p.text)
         print "Sent password " + str(p.status_code)
         if p.status_code != 200:
            print "Cannot Log in " + str( url)
            raise IOError
         else:
            print "Login repsonse code: " + str(j.get('code'))
            if j.get('code') != 0:
               raise IOError("Incorrect password site " + str(url) + " and user " + str(self.m_login_payload['account']))
            else:
               # Store station URL
               self.m_goodwe_station_url = self.m_goodwe_url + j.get('data').get('redirect')
               print "Station URL found: " + str(self.m_goodwe_station_url)

         

   #--------------------------------------------------------------------------
   def read_sample_data( self):
   # Read the data. When a failure is found, it is tried upto 3 times. After 
   # that, an error is logged.
   #
      tries = 0
      
      while True:
         try:
            sample = self._read_data()
            self.gwData = goodweData.goodweData( sample)
            for subscriber in self.subscribers:
               subscriber( self.gwData.get_sample().get_temperature())
            return self.gwData.get_sample()
         except EOFError, ex:
            # Try to create a new session
            print "Session authentication ended, creating new session"
            tries += 1
            try:
               self.create_session()
            except Exception, ex:
               print "Failed to create new session: " + str(ex)
         except Exception, ex:
            print "Error reading data. Trying again. Error: " + str(ex)
            tries += 1

         if tries > 3:
            print "Cannot read data after " + str(tries) + " tries, giving up"
            raise ValueError

         
   #--------------------------------------------------------------------------
   def is_online( self):
      '''Is online?'''
      if self.gwData:
         return self.gwData.is_online()
      else:
         return False
      
   #--------------------------------------------------------------------------
   def initialize( self):
      '''Initialize'''
      pass
      
   #--------------------------------------------------------------------------
   def terminate( self):
      '''Terminate'''
      pass
      
   #--------------------------------------------------------------------------
   def _read_data( self):
   # Do the actual read from the URL
   #
      if self.m_session:
         r = self.m_session.get( self.m_goodwe_station_url, 
                                 headers = dict( referer = self.m_goodwe_station_url))
         return r.content
      return ""
                  
#---------------- End of file ------------------------------------------------
