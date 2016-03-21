import requests
import time
  
class pvoutput :

   #--------------------------------------------------------------------------
   def __init__( self, url, system_id, api_key):
      self.m_url = url
      self.m_system_id = system_id
      self.m_api_key = api_key
      
   #--------------------------------------------------------------------------
   def post_data( self, pgrid, temperature, voltage, interval = 0):
      t = time.gmtime(time.time()-interval)

      header = {'X-Pvoutput-Apikey' : self.m_api_key,
                'X-Pvoutput-SystemId' : self.m_system_id}
      post = {'d' : str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2),
              't' : str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2),
              'v2' : str(pgrid),
              'v5' : str(temperature),
              'v6' : str(voltage)}
      print str(post)
      r = requests.requests.post(self.m_url, headers=header, data=post, timeout=20)
     



