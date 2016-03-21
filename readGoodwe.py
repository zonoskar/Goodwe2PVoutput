import requests

class readGoodwe :

   #--------------------------------------------------------------------------
   def __init__(self, url, station_id):
      self.m_url = url
      self.m_station_id = station_id
      
      
   #--------------------------------------------------------------------------
   def read_data( self):
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
      r = requests.requests.get( url, timeout=20)
      return r.content
                  
