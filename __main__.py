import readGoodwe
import goodweData
import pvoutput
import csvoutput
import processData
import time

# sid: The system ID as known on goodwe-power.com.
sid = '[Your system ID on Goodwe-poer.com]'

# sys_id: The system ID as known on PVoutput
sys_id = '[your system ID on PVoutput.org]'

# API key otained from PVoutput. You have to request this.
api_key = '[Your PVoutput API key (generate one)]'

# CSV logging directory
csv_dir = '[Directory where you want the CSV files]'

def mainloop( goodwe, pvoutput, csv):
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
# objects needed and sets the URL and system IDs. These are defined at the
# start of this file
#
   # These URLs should be okay for Goodwe-power and PVoutput.org (and yes, there
   # is a spelling error in the goodwe URL).
   goodwe_url = 'http://goodwe-power.com/PowerStationPlatform/PowerStationReport/InventerDetail'
   pvoutput_url = 'http://pvoutput.org/service/r2/addstatus.jsp'
   
   goodwe = readGoodwe.readGoodwe( goodwe_url, sid)
   pvoutput = pvoutput.pvoutput( pvoutput_url, sys_id, api_key)
   csv = csvoutput.csvoutput( csv_dir, 'Goodwe_PV_data')
   process = processData.processData( pvoutput)
   
   # Perform main loop
   mainloop( goodwe, pvoutput, csv)
