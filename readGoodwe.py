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
      self.m_login_url = url+login_url
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
      payload = {
         'account': username,
         'pwd': password }
      url = self.m_login_url

      with requests.Session() as self.m_session:
         print "login :" + url
         p = self.m_session.post( url, data=payload)
         j=json.loads(p.text)
         print "Sent password " + str(p.status_code)
         if p.status_code != 200:
            print "Cannot Log in " + str( url)
            raise IOError
         else:
            print "Login repsonse code: " + str(j.get('code'))
            if j.get('code') != 0:
               raise IOError("Incorrect password site " + str(url) + " and user " + str(username))
            else:
               self.m_goodwe_url += j.get('data').get('redirect')
               print "Station URL found: " + str(self.m_goodwe_url)

         

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
         except Exception, ex:
            tries += 1
            if tries > 3:
               print "Cannot read data after " + str(tries) + " tries: " + str(ex)
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
         r = self.m_session.get( self.m_goodwe_url, 
                                 headers = dict( referer = self.m_goodwe_url))
         return r.content
      return ""
                  
#---------------- End of file ------------------------------------------------
