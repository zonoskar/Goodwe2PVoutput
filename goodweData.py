import goodweSample
  
class goodweData :

   #--------------------------------------------------------------------------
   def __init__( self, urlData):
   #Initialization of the goodweData class. All data members are set
   #to default values. Then the urlData is filtered and parsed
      print "Test2"
      try:
         self.m_sample = goodweSample.goodweSample()
      except Exception, ex: 
         print "Error:" +str(ex)
      print "Test"
      
      try:
         filteredData = self.filter_data( urlData)
	 print filteredData
      except Exception, arg:
         print "Filter data Error: " + str(arg)
      try:
         self.parse_data( filteredData)
      except Exception, arg:
         print "Parse data Error: " + str(arg)

   #--------------------------------------------------------------------------
   def parse_data( self, filteredData):
   #Parses the filtered data. This will yield nice and usable
   #data member values.
   #
      self.m_sample.set_line( filteredData[0])
      self.m_sample.set_inverter_status( filteredData[1])
      self.m_sample.set_inverter_sn( filteredData[2])
      self.m_sample.set_description( filteredData[3])
      self.m_sample.set_error( filteredData[8])

      #Values that I'm not using (or don't know what they are
      self.m_sample.set_vbattery( filteredData[15].replace(' ', ''))
      self.m_sample.set_ibattery( filteredData[16].replace(' ', ''))
      self.m_sample.set_soc( filteredData[17].replace(' ', ''))
      self.m_sample.set_load( filteredData[18].replace(' ', ''))

      self.m_sample.set_pgrid( self._convert_line_to_float(filteredData[4]))
      self.m_sample.set_eday( self._convert_line_to_float(filteredData[5]))
      self.m_sample.set_etotal( self._convert_line_to_float(filteredData[6]))
      self.m_sample.set_htotal( self._convert_line_to_float(filteredData[7]))
      # Only select 1 significant digit after .
      self.m_sample.set_temperature( self._convert_line_to_float(filteredData[14][0:filteredData[14].find('.')+2]))

      #multi line values, separated by '/'
      v = filteredData[9].split('/')
      if len(v) == 2:
         for frac in range(len(v)):
            self.m_sample.set_vpv( frac, self._convert_line_to_float(v[frac]))

      i = filteredData[10].split('/')
      if len(i) == 2:
         for frac in range(len(i)):
            self.m_sample.set_ipv( frac, self._convert_line_to_float(i[frac]))

      v = filteredData[11].split('/')
      if len(v) == 3:
         for frac in range(len(v)):
            self.m_sample.set_vac( frac, self._convert_line_to_float(v[frac]))

      i = filteredData[12].split('/')
      if len(i) == 3:
         for frac in range(len(i)):
            self.m_sample.set_iac( frac, self._convert_line_to_float(i[frac]))

      f = filteredData[13].split('/')
      if len(f) == 3:
         for frac in range(len(f)):
            self.m_sample.set_fac( frac, self._convert_line_to_float(f[frac]))

      self.m_sample.set_consume_day( self._convert_line_to_float(filteredData[19]))
      self.m_sample.set_consume_total( self._convert_line_to_float(filteredData[20]))

      # Calculate efficiency (PowerAC / powerDC)
      try:
         ppv = ((self.m_sample.get_vpv(0) * self.m_sample.get_ipv(0)) + (self.m_sample.get_vpv(1) * self.m_sample.get_ipv(1)))
         if ppv > 0.0:
            self.m_sample.set_efficiency( self.m_sample.get_pgrid() / ppv)
      except Exception, arg:
         print "Calculate Efficiency Error: " + str(arg)
         self.m_sample.set_efficiency( 0.0)


   #--------------------------------------------------------------------------
   def filter_data( self, response):
   #Filters the URL data. This will select the correct table from the 
   #URL data and strip all units from the data strings ready to be 
   #converted to float or integers.
   #
      # Select from the HTTP data the table row with DG_Item
      title = response[response.find('<title>')+7:response.find('</title>')]
      table = response[response.find('id="tab_big"'):]
      table = table[table.find('<tr>')+5:]
      table = table[table.find('<tr>')+5:]
      table = table[:table.find('</tr>')]
      table = table.replace(' ', '')

      # Split the table row in columns using the <td> HTTP tag
      r = table.split('<td>')
      l = []
      for line in r:
         if '</td>' in line:
            line=line.replace('</td>', '')
            line=line.replace('\n', '')
            line=line.replace('\r', '')
            l.append(line)
	    
      if len(l) != 21:
          print title
          print "Response from Goodwe does not contain all data (len=" + str(len(l)) + ") : " + str(l)
	  
      return l

   #--------------------------------------------------------------------------
   def _convert_line_to_float( self, line):
      retval = 0.0
      try:
	 line=line.replace('A', '')
	 line=line.replace('V', '')
	 line=line.replace('K', '')
	 line=line.replace('W', '')
	 line=line.replace('h', '')
	 line=line.replace('k', '')
	 line=line.replace('H', '')
	 line=line.replace('z', '')
	 line=line.replace('%', '')
	 line=line.replace(' ', '')
         retval = float(line)
      except(ValueError):
	 retval = 0.0
	 return retval

      return retval
    


   #--------------------------------------------------------------------------
   def to_csv_string( self):
   #Creates a string representation of the class, separated by ','.
   #
      return str(self.m_sample.to_csv_string())


   #--------------------------------------------------------------------------
   def get_csv_header( self):
   #Returns the CSV header format string.
   #
      return "Date, Time, Line, Inverter_SN, Inverter_status, Pgrid, Eday, Etotal, Htotal, Error, Vpv1, Vpv2, Ipv1, Ipv2, Vac1, Vac2, Vac3, Iac1, Iac2, Iac3, Fac1, Fac2, Fac3, Temperature, Vbattery, Ibattery, SOC, Vload, Iload, Pload, Consume_day, Consume_total, Efficiency"


   #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_sample.is_inverter_status('Normal')) and (abs(self.m_sample.get_vpv(0)+self.m_sample.get_vpv(1)) > 0.01))
      

   #--------------------------------------------------------------------------
   def is_identical( self, gw):
   #Compares select data members to determine if two instances of the
   #goodweData class are identical
   #
      return self.m_sample.is_identical(gw)


   #--------------------------------------------------------------------------
   def interpolate( self, gw):
   #Interpolates two goodweData class instances by using linear 
   #interpolation. This will yield a nicer graph in PVoutput.org
   #
      igw = gw
      
      igw.set_vpv(0, (self.m_sample.get_vpv(0) + gw.get_vpv(0)) / 2)
      igw.set_vpv(1, (self.m_sample.get_vpv(1) + gw.get_vpv(1)) / 2)
      igw.set_ipv(0, (self.m_sample.get_ipv(0) + gw.get_ipv(0)) / 2)
      igw.set_ipv(1, (self.m_sample.get_ipv(1) + gw.get_ipv(1)) / 2)
      igw.set_vac(0, (self.m_sample.get_vac(0) + gw.get_vac(0)) / 2)
      igw.set_vac(1, (self.m_sample.get_vac(1) + gw.get_vac(1)) / 2)
      igw.set_vac(2, (self.m_sample.get_vac(2) + gw.get_vac(2)) / 2)
      igw.set_iac(0, (self.m_sample.get_iac(0) + gw.get_iac(0)) / 2)
      igw.set_iac(1, (self.m_sample.get_iac(1) + gw.get_iac(1)) / 2)
      igw.set_iac(2, (self.m_sample.get_iac(2) + gw.get_iac(2)) / 2)
      igw.set_fac(0, (self.m_sample.get_fac(0) + gw.get_fac(0)) / 2)
      igw.set_fac(1, (self.m_sample.get_fac(1) + gw.get_fac(1)) / 2)
      igw.set_fac(2, (self.m_sample.get_fac(2) + gw.get_fac(2)) / 2)
      igw.set_pgrid( (self.m_sample.get_pgrid() + gw.get_pgrid()) / 2)
      igw.set_eday( (self.m_sample.get_eday() + gw.get_eday()) / 2)
      igw.set_etotal( (self.m_sample.get_etotal() + gw.get_etotal()) / 2)
      igw.set_htotal( (self.m_sample.get_htotal() + gw.get_htotal()) / 2)
      igw.set_temperature( (self.m_sample.get_temperature() + gw.get_temperature()) / 2)
      igw.set_efficiency( (self.m_sample.get_efficiency() + gw.get_efficiency()) / 2)
      
      return igw
      

   #--------------------------------------------------------------------------
   def get_vpv0( self):
      return self.m_sample.get_vpv(0)
   def get_vpv1( self):
      return self.m_sample.get_vpv(1)
   def get_ipv0( self):
      return self.m_sample.get_ipv(0)
   def get_ipv1( self):
      return self.m_sample.get_ipv(1)
   def get_vac0( self):
      return self.m_sample.get_vac(0)
   def get_vac1( self):
      return self.m_sample.get_vac(1)
   def get_vac2( self):
      return self.m_sample.get_vac(2)
   def get_iac0( self):
      return self.m_sample.get_iac(0)
   def get_iac1( self):
      return self.m_sample.get_iac(1)
   def get_iac2( self):
      return self.m_sample.get_iac(2)
   def get_fac0( self):
      return self.m_sample.get_fac(0)
   def get_fac1( self):
      return self.m_sample.get_fac(1)
   def get_fac2( self):
      return self.m_sample.get_fac(2)
   def get_pgrid( self):
      return self.m_sample.get_pgrid()
   def get_eday( self):
      return self.m_sample.get_eday()
   def get_temperature( self):
      return self.m_sample.get_temperature()
   def get_etotal( self):
      return self.m_sample.get_etotal()
   def get_htotal( self):
      return self.m_sample.get_htotal()
   def get_efficiency( self):
      return self.m_sample.get_efficiency()


   #--------------------------------------------------------------------------
   def to_string( self):
      return self.m_sample.to_string()
   
   def to_short_string( self):
      return self.m_sample.to_short_string()
   
   
#---------------- End of file ------------------------------------------------
