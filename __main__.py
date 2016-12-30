from Goodwe2PVoutput import readGoodwe
from Goodwe2PVoutput import goodweConfig
from Goodwe2PVoutput import goodweData
from Goodwe2PVoutput import pvoutput
from Goodwe2PVoutput import csvoutput
from Goodwe2PVoutput import processData
import time
import getpass
import os
import logging
import argparse

def mainloop( goodwe, process, csv):
# Main processing loop
#
   # Do for ever.
   while True:
      interval = 4 * 60
      try: # Read Goodwe data from goodwe-power.com
         r = goodwe.read_data()
      except Exception as arg:
         logging.warning("Read data Error: " + str(arg))
      else:
         try: # Convert the URL data to usable data oject
            gw = goodweData.goodweData( r)
         except Exception as arg:
            logging.warning("Convert data Error: " + str(arg))
         else:
            if gw.is_online():
               # write CSV file
               csv.write_data( gw)
               process.processSample( gw)
            else:
               # Wait for the inverter to come online
               logging.info("Inverter is not online: " + gw.to_string())
               interval = 20 * 60
               csv.reset()
               process.reset()

      # Wait for the next sample
      logging.debug("sleep " + str(interval) + " seconds before next sample")
      time.sleep(interval)



if __name__ == "__main__":
# Main entry point for the Goodwe to PVoutput logging script. Creates the
# objects needed and sets the URL and system IDs. These are read from the
# config file in ${HOME}/.goodwe2pvoutput
#

   # Parse command line arguments
   parser = argparse.ArgumentParser(description="Upload Goodwe power invertor data to PVOutput.org")
   parser.add_argument("--log", "-l", help="set log level", default="debug")
   args = parser.parse_args()

   # Configure the logging
   numeric_level = getattr(logging, args.log.upper(), None)
   if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % loglevel)
   logging.basicConfig(format='%(levelname)8s:%(message)s', level=numeric_level)

   home = os.environ['HOME']
   config = goodweConfig.goodweConfig(home+'/.goodwe2pvoutput')
   config.to_string()

   goodwe = readGoodwe.readGoodwe( config.get_goodwe_url(), config.get_goodwe_loginUrl(), config.get_goodwe_system_id())
   pvoutput = pvoutput.pvoutput( config.get_pvoutput_url(), config.get_pvoutput_system_id(), config.get_pvoutput_api())
   csv = csvoutput.csvoutput( config.get_csv_dir(), 'Goodwe_PV_data')
   process = processData.processData( pvoutput)

   # Request password for Goodwe-power.com
   password = config.get_goodwe_password()
   if password is None:
       passwd_text = 'Supply password for ' + str(config.get_goodwe_loginUrl()) + ': '
       password = getpass.getpass( passwd_text)
   goodwe.login( config.get_goodwe_user_id(), password)

   # Perform main loop
   mainloop( goodwe, process, csv)
