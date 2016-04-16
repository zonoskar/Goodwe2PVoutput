import requests
import time
  
class pvoutput :

   #--------------------------------------------------------------------------
   def __init__( self, url, system_id, api_key):
   # PVoutput logging class. This class logs the inverter data to PVoutput
   # using the supplied URL, API key and system ID.
   #
      self.m_url = url
      self.m_system_id = system_id
      self.m_api_key = api_key
      
   #--------------------------------------------------------------------------
   def post_data( self, eday, pgrid, temperature, voltage):
   # Post the inverter data to PVoutput. The eday value from Goodwe-power.com
   # is in kWh, but PVoutput.org wants this value in Wh, so it is multiplied 
   # by 1000.
   #
      t = time.localtime(time.time())
      header = {'X-Pvoutput-Apikey' : self.m_api_key,
                'X-Pvoutput-SystemId' : self.m_system_id}
      post = {'d' : str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2),
              't' : str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2),
              'v1' : str(eday*1000),
              'v2' : str(pgrid),
              'v5' : str(temperature),
              'v6' : str(voltage)}
      print str(post)
      try:
         r = requests.requests.post(self.m_url, headers=header, data=post, timeout=20)
         print r
      except Exception, arg:
         print "POST data Error: " + str(arg)
         



