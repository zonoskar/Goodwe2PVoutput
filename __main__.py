import readGoodwe
import goodweData
import pvoutput
import csvoutput
import time

def mainloop( goodwe, pvoutput, csv):
   interpolate = False
   write_header = True
   prev_gw = None

   # Do for ever.
   while True:
      try:
	 r = goodwe.read_data()
	 gw = goodweData.goodweData( r)

	 if gw.is_online():
	    interval = 4*60
            csv.write_data( gw, write_header)
	    write_header = False

            print "Measured    : " + gw.to_string()

	    if gw.is_identical( prev_gw):
               if interpolate:
        	  pvoutput.post_data( prev_gw.m_pgrid, prev_gw.m_temperature, prev_gw.m_vpv1 + prev_gw.m_vpv2, interval = interval)
	       interpolate = True
	    else:
	       if interpolate:
        	  gw1 = gw.interpolate( prev_gw)
        	  pvoutput.post_data( gw1.m_pgrid, gw1.m_temperature, gw1.m_vpv1 + gw1.m_vpv2, interval = interval)
		  interpolate = False
        	  time.sleep(60)
        	  interval = 3*60

               pvoutput.post_data( gw.m_pgrid, gw.m_temperature, gw.m_vpv1 + gw.m_vpv2)
	 else:
            print "Inverter is not online"
	    interval = 20*60
	    prev_gw = None
	    write_header = True
      except:
	 print "read error"

      prev_gw = gw
      print "sleep " + str(interval) + " seconds before next sample"
      time.sleep(interval)



if __name__ == "__main__":
   goodwe_url = 'http://goodwe-power.com/PowerStationPlatform/PowerStationReport/InventerDetail'
   sid = 'da892c15-a156-4006-bd1d-5dacec1b64c3'
   pvoutput_url = 'http://pvoutput.org/service/r2/addstatus.jsp'
   sys_id = '40669'
   api_key = 'e804c1db643280f2c316a609133f1301f14462ad'
   csv_dir = '/media/pi/Data/PVoutput'
   interval=4*60
   
   goodwe = readGoodwe.readGoodwe( goodwe_url, sid)
   pvoutput = pvoutput.pvoutput( pvoutput_url, sys_id, api_key)
   csv = csvoutput.csvoutput( csv_dir, 'Goodwe_PV_data')
   
   # Perform main loop
   mainloop( goodwe, pvoutput, csv)
