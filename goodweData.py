import goodweSample
  
class goodweData :

   #--------------------------------------------------------------------------
   def __init__( self, urlData):
   #Initialization of the goodweData class. All data members are set
   #to default values. Then the urlData is filtered and parsed
      try:
         self.m_sample = goodweSample.goodweSample()
      except Exception, ex: 
         print "Error:" +str(ex)
      
      try:
         filteredData = self.filter_data( urlData)
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
  #    self.m_sample.set_vbattery( filteredData[15].replace(' ', ''))
  #    self.m_sample.set_ibattery( filteredData[16].replace(' ', ''))
  #    self.m_sample.set_soc( filteredData[17].replace(' ', ''))
  #    self.m_sample.set_load( filteredData[18].replace(' ', ''))

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

      self.m_sample.set_consume_day( self._convert_line_to_float(filteredData[15]))
      self.m_sample.set_consume_total( self._convert_line_to_float(filteredData[16]))

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
	    
      if len(l) != 17:
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
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_sample.is_inverter_status('Normal')) and (abs(self.m_sample.get_vpv(0)+self.m_sample.get_vpv(1)) > 0.01))
      

   #--------------------------------------------------------------------------
   def is_identical( self, sample):
   #Compares select data members to determine if two instances of the
   #goodweData class are identical
   #
      return self.m_sample.is_identical(sample.m_sample)


   #--------------------------------------------------------------------------
   def get_sample( self):
      return self.m_sample
      
      
   #--------------------------------------------------------------------------
   def to_string( self):
      return self.m_sample.to_string()
   

   #--------------------------------------------------------------------------
   def to_short_string( self):
      return self.m_sample.to_short_string()
   
   
#---------------- End of file ------------------------------------------------
