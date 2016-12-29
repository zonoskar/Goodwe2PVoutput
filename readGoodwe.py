import requests

class readGoodwe :

   #--------------------------------------------------------------------------
   def __init__(self, url, login_url, station_id):
   # Goodwe-power reading class. Reads the Goodwe-power.com website
   # from the specified URL and station ID.
   #
      self.m_goodwe_url = url
      self.m_login_url = login_url
      self.m_station_id = station_id
      self.m_session = None


   #--------------------------------------------------------------------------
   def login(self, username, password):
   # Log in Goodwe-power web site.
   #
      payload = {
         'username': username,
         'password': password }

      with requests.Session() as self.m_session:
         p = self.m_session.post( self.m_login_url, data=payload)
         if p.status_code != 200:
            print "Cannot Log in " + str(self.m_login_url)
            raise IOError
         if 'incorrect' in p.text:
            print "Incorrect password for user " + str(username)
            raise IOError
         print "User " + str(username) + " Logged in"


   #--------------------------------------------------------------------------
   def read_data( self):
   # Read the data. When a failure is found, it is tried upto 3 times. After
   # that, an error is logged.
   #
      url = self.m_goodwe_url + "?ID=" + self.m_station_id
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
      if self.m_session:
         r = self.m_session.get( url, timeout=20)
      return r.content

