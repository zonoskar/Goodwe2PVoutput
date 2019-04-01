import goodweConfig
import GoodweFactory
import pvoutput
import csvoutput
import time
import getpass
import os

def mainloop( goodwe, pvoutput, csv, process):
# Main processing loop
#
   # Do for ever.
   try:
      while True:
         interval = 5.0*60
         try: # Read Goodwe data from goodwe-power.com
#            print "read sample"
            gw = goodwe.read_sample_data()
         except Exception, arg:
            interval = 1.0*60
            print "Read data Error: " + str(arg)
         else:
            if goodwe.is_online():
               # write CSV file
#               print "CSV sample"
               csv.write_data( gw)
#               print "Process sample"
               process.processSample( gw)
            else:
               # Wait for the inverter to come online
               print "Inverter is not online: " + gw.to_string()
               interval = 30.0*60
               csv.reset()
               process.reset()

         # Wait for the next sample
#        print "sleep " + str(interval) + " seconds before next sample"
         time.sleep(interval)
   except KeyboardInterrupt:
      print "Keyboard Initerrupt"
      goodwe.terminate()
      


if __name__ == "__main__":
# Main entry point for the Goodwe to PVoutput logging script. Creates the
# objects needed and sets the URL and system IDs. These are read from the
# config file in ${HOME}/.goodwe2pvoutput
#
   home = os.environ['HOME']
   configfile = os.path.join(home,'.goodwe2pvoutput')
   config = goodweConfig.goodweConfig( configfile)
   factory = GoodweFactory.GoodweFactory( config)
   config.to_string()

   pvoutput = pvoutput.pvoutput( config.get_pvoutput_url(), 
                                 config.get_pvoutput_system_id(), 
                                 config.get_pvoutput_api())
   csv = csvoutput.csvoutput( config.get_csv_dir(), 'Goodwe_PV_data')
   goodwe, process = factory.create( pvoutput)

   try:
      goodwe.initialize()
      print config.get_input_source() + " initialized"
   except Exception, ex:
      print ex

   if config.get_temp_monitor():
      print "Setting up temperature monitoring."
      import tempMonitor
      tempMonitor.tempMonitor( goodwe, config.get_gpio_fan_pins())

   # Perform main loop
   mainloop( goodwe, pvoutput, csv, process)

#---------------- End of file ------------------------------------------------
