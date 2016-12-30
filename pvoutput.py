import logging
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
   def post_data( self, gw):
   # Post the inverter data to PVoutput. The eday value from Goodwe-power.com
   # is in kWh, but PVoutput.org wants this value in Wh, so it is multiplied
   # by 1000.
   #

      # Extended parameters.
      p1 = gw.m_vpv[0] * gw.m_ipv[0] * gw.m_efficiency
      p2 = gw.m_vpv[1] * gw.m_ipv[1] * gw.m_efficiency
      vs = 0
      vac = 0
      for v in gw.m_vac:
         if v > 0:
            vac = vac + v
            vs = vs + 1

      if vs > 0:
         vac = vac / vs

      t = time.localtime(time.time())
      header = {'X-Pvoutput-Apikey' : self.m_api_key,
                'X-Pvoutput-SystemId' : self.m_system_id}
      post = {'d' : str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2),
              't' : str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2),
              'v1' : str(gw.m_eday*1000),
              'v2' : str(gw.m_pgrid),
#               'v5' : str(gw.m_temperature),   # Goodwe reports panel temperature, PVOutput expects environmental temperature
              'v6' : str(gw.m_vpv[0] + gw.m_vpv[1]),
              'v7' : str(gw.m_vpv[0]),
              'v8' : str(gw.m_vpv[1]),
              'v9' : str(p1),
              'v10' : str(p2),
              'v11' : str(vac),
              'v12' : str(gw.m_efficiency)}
      logging.debug(str(post))
      try:
         r = requests.post(self.m_url, headers=header, data=post, timeout=20)
      except Exception as arg:
         logging.error("POST data Error: " + str(arg))




