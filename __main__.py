import readGoodwe
import goodweConfig
import goodweData
import goodweUsb
import pvoutput
import csvoutput
import processData
import processNone
import processData2
import time
import getpass
import os

def mainloop( goodwe, pvoutput, csv, process):
# Main processing loop
#
   # Do for ever.
   while True:
      interval = 4.0*60
      try: # Read Goodwe data from goodwe-power.com
         gw = goodwe.read_sample_data()
      except Exception, arg:
         interval = 1.0*60
         print "Read data Error: " + str(arg)
      else:
         if goodwe.is_online():
            # write CSV file
            csv.write_data( gw)
            process.processSample( gw)
         else:
            # Wait for the inverter to come online
            print "Inverter is not online: " + gw.to_string()
            interval = 10.0*60
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

   pvoutput = pvoutput.pvoutput( config.get_pvoutput_url(), 
                                 config.get_pvoutput_system_id(), 
                                 config.get_pvoutput_api())
   csv = csvoutput.csvoutput( config.get_csv_dir(), 'Goodwe_PV_data')

   if config.get_input_source() == 'URL':
      goodwe = readGoodwe.readGoodwe( config.get_goodwe_url(), 
                                      config.get_goodwe_loginUrl(), 
                                      config.get_goodwe_system_id())
      # Request password for Goodwe-power.com
      passwd_text = 'Supply password for ' + str(config.get_goodwe_loginUrl()) + ': '
      password = getpass.getpass( passwd_text)
      goodwe.login( config.get_goodwe_user_id(), password)
   
      if config.get_spline_fit():
         process = processData2.processData2( pvoutput)
      else:
         process = processData.processData( pvoutput)
      
   if config.get_input_source() == 'USB':
      goodwe = goodweUsb.goodweUsb( 'test', ' ', 0x0084)
      try:
         goodwe.initialize()
         print "USB connection initialized"
      except Exception, ex:
         print ex
         print "Connect USB cable to the inverter please or wait until the inverter is online"

      process = processNone.processNone( pvoutput)

   # Perform main loop
   mainloop( goodwe, pvoutput, csv, process)


#---------------- End of file ------------------------------------------------
