import readGoodwe
import goodweConfig
import goodweData
import pvoutput
import csvoutput
import processData
import time
import getpass
import os

def mainloop( goodwe, process, csv):
# Main processing loop
#
   # Do for ever.
   while True:
      interval = 4.0*60
      try: # Read Goodwe data from goodwe-power.com
         r = goodwe.read_data()
      except Exception, arg:
         print "Read data Error: " + str(arg)
      else:
         try: # Convert the URL data to usable data oject
            gw = goodweData.goodweData( r)
         except Exception, arg:
            print "Convert data Error: " + str(arg)
         else:
            if gw.is_online():
               # write CSV file
               csv.write_data( gw)
               process.processSample( gw)
            else:
               # Wait for the inverter to come online
               print "Inverter is not online: " + gw.to_string()
               interval = 20.0*60
               csv.reset()
               process.reset()

      # Wait for the next sample
      print "sleep " + str(interval) + " seconds before next sample"
      time.sleep(interval)



if __name__ == "__main__":
# Main entry point for the Goodwe to PVoutput logging script. Creates the
# objects needed and sets the URL and system IDs. These are read from the
# config file in ${HOME}/.goodwe2pvoutput
#
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
