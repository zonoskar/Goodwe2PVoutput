import requests

class readGoodwe :

   #--------------------------------------------------------------------------
   def __init__(self, url, station_id):
   # Goodwe-power reading class. Reads the Goodwe-power.com website
   # from the specified URL and station ID.
   #
      self.m_url = url
      self.m_station_id = station_id
      
      
   #--------------------------------------------------------------------------
   def read_data( self):
   # Read the data. When a failure is found, it is tried upto 3 times. After 
   # that, an error is logged.
   #
      url = self.m_url + "?ID=" + self.m_station_id
      tries = 0
      
      while True:
         try:
            r = self._read_data( url)
            return r
         except:
            tries += 1
            if tries > 3:
               print "Cannot read data after " + str(tries) + " tries."
               raise ValueError
         
      
   #--------------------------------------------------------------------------
   def _read_data( self, url):
   # Do the actual read from the URL
   #
      r = requests.requests.get( url, timeout=20)
      return r.content
                  
