  
class goodweData :

   #--------------------------------------------------------------------------
   def __init__( self, urlData):
   #Initialization of the goodweData class. All data members are set
   #to default values. Then the urlData is filtered and parsed
      self.m_line = ''
      self.m_inverter_sn = ''
      self.m_description = ''
      self.m_inverter_status = ''
      self.m_error = ''
      self.m_vbattery = ''
      self.m_ibattery = ''
      self.m_soc = ''
      self.m_pgrid = 0.0
      self.m_eday = 0.0
      self.m_etotal = 0.0
      self.m_htotal = 0.0
      self.m_temperature = 0.0
      self.m_load = ''

      self.m_vpv = []
      self.m_ipv = []
      self.m_vac = []
      self.m_iac = []
      self.m_fac = []

      for i in range(3):
         self.m_vpv.append(0.0)
         self.m_ipv.append(0.0)
         self.m_vac.append(0.0)
         self.m_iac.append(0.0)
         self.m_fac.append(0.0)

      self.m_consume_day = 0.0
      self.m_consume_total = 0.0
      self.m_efficiency = 0.0
      
      try:
         filteredData = self.filter_data( urlData)
#	 print filteredData
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
      self.m_line = filteredData[0]
      self.m_inverter_status = filteredData[1]
      self.m_inverter_sn = filteredData[2]
      self.m_description = filteredData[3]
      self.m_error = filteredData[8]

      #Values that I'm not using (or don't know what they are
      self.m_vbattery = filteredData[15].replace(' ', '') # 0.0/0.0V
      self.m_ibattery = filteredData[16].replace(' ', '') # 0.0/0.0A
      self.m_soc = filteredData[17].replace(' ', '') # 0/0%
      self.m_load = filteredData[18].replace(' ', '') # 0.0V/0.0A/0.000KW

      self.m_pgrid = self._convert_line_to_float(filteredData[4])
      self.m_eday = self._convert_line_to_float(filteredData[5])
      self.m_etotal = self._convert_line_to_float(filteredData[6])
      self.m_htotal = self._convert_line_to_float(filteredData[7])
      # Only select 1 significant digit after .
      self.m_temperature = self._convert_line_to_float(filteredData[14][0:filteredData[14].find('.')+2])

      #multi line values, separated by '/'
      v = filteredData[9].split('/')
      if len(v) == 2:
         for frac in range(len(v)):
            self.m_vpv[frac] = self._convert_line_to_float(v[frac])

      i = filteredData[10].split('/')
      if len(i) == 2:
         for frac in range(len(i)):
            self.m_ipv[frac] = self._convert_line_to_float(i[frac])

      v = filteredData[11].split('/')
      if len(v) == 3:
         for frac in range(len(v)):
            self.m_vac[frac] = self._convert_line_to_float(v[frac])

      i = filteredData[12].split('/')
      if len(i) == 3:
         for frac in range(len(i)):
            self.m_iac[frac] = self._convert_line_to_float(i[frac])

      f = filteredData[13].split('/')
      if len(f) == 3:
         for frac in range(len(f)):
            self.m_fac[frac] = self._convert_line_to_float(f[frac])

      self.m_consume_day = self._convert_line_to_float(filteredData[19])
      self.m_consume_total = self._convert_line_to_float(filteredData[20])

      # Calculate efficiency (PowerAC / powerDC)
      try:
         ppv = ((self.m_vpv[0] * self.m_ipv[0]) + (self.m_vpv[1] * self.m_ipv[1]))
         if ppv > 0.0:
            self.m_efficiency = self.m_pgrid / ppv
      except Exception, arg:
         print "Calculate Efficiency Error: " + str(arg)


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
   def to_short_string( self):
   #Creates a string repesentation of the class
   #
      return "S/N: " + str(self.m_inverter_sn) + " P:" + str(self.m_pgrid) + " E:" + str(self.m_eday) + " V:" + str(self.m_vpv[0]+self.m_vpv[1])


   #--------------------------------------------------------------------------
   def to_string( self):
   #Creates a string repesentation of the class
   #
      return self.to_csv_string().replace(',', '')


   #--------------------------------------------------------------------------
   def to_csv_string( self):
   #Creates a string repesentation of the class, separated by ','.
   #
      return str(self.m_line) + ", " + str(self.m_inverter_sn) + ", " + str(self.m_description) + ", " + str(self.m_inverter_status) + ", " + str(self.m_pgrid) + ", " + str(self.m_eday) + ", " + str(self.m_etotal) + ", " + str(self.m_htotal) + ", " + str(self.m_error) + ", " + str(self.m_vpv[0]) + ", " + str(self.m_vpv[1]) + ", " + str(self.m_ipv[0]) + ", " + str(self.m_ipv[1]) + ", " + str(self.m_vac[0]) + ", " + str(self.m_vac[1]) + ", " + str(self.m_vac[2]) + ", " + str(self.m_iac[0]) + ", " + str(self.m_iac[1]) + ", " + str(self.m_iac[2]) + ", " + str(self.m_fac[0]) + ", " + str(self.m_fac[1]) + ", " + str(self.m_fac[2]) + ", " + str(self.m_temperature) + ", " + str(self.m_consume_day) + ", " + str(self.m_consume_total) + ", " + str(self.m_efficiency)


   #--------------------------------------------------------------------------
   def get_csv_header( self):
   #Returns the CSV header format string.
   #
      return "Date, Time, Line, Inverter_SN, Inverter_status, Pgrid, Eday, Etotal, Htotal, Error, Vpv1, Vpv2, Ipv1, Ipv2, Vac1, Vac2, Vac3, Iac1, Iac2, Iac3, Fac1, Fac2, Fac3, Temperature, Vbattery, Ibattery, SOC, Vload, Iload, Pload, Consume_day, Consume_total, Efficiency"


   #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return ((self.m_inverter_status == 'Normal') and (abs(self.m_vpv[0]+self.m_vpv[1]) > 0.01))
      

   #--------------------------------------------------------------------------
   def is_identical( self, gw):
   #Compares select data members to determine if two instances of the
   #goodweData class are identical
   #
      eps = 0.05
      if not gw:
         return False
         
      if (abs(self.m_vpv[0] - gw.m_vpv[0]) < eps) and \
         (abs(self.m_vpv[1] - gw.m_vpv[1]) < eps) and \
         (abs(self.m_ipv[0] - gw.m_ipv[0]) < eps) and \
         (abs(self.m_ipv[1] - gw.m_ipv[1]) < eps) and \
         (abs(self.m_pgrid  - gw.m_pgrid)  < eps) and \
         (abs(self.m_vac[0] - gw.m_vac[0]) < eps) and \
         (abs(self.m_vac[1] - gw.m_vac[1]) < eps) and \
         (abs(self.m_vac[2] - gw.m_vac[2]) < eps) and \
         (abs(self.m_iac[0] - gw.m_iac[0]) < eps) and \
         (abs(self.m_iac[1] - gw.m_iac[1]) < eps) and \
         (abs(self.m_iac[2] - gw.m_iac[2]) < eps) and \
         (abs(self.m_fac[0] - gw.m_fac[0]) < eps) and \
         (abs(self.m_fac[1] - gw.m_fac[1]) < eps) and \
         (abs(self.m_fac[2] - gw.m_fac[2]) < eps) :
         return True
         
      return False      


   #--------------------------------------------------------------------------
   def interpolate( self, gw):
   #Interpolates two goodweData class instances by using linear 
   #interpolation. This will yield a nicer graph in PVoutput.org
   #
      igw = gw
      
      igw.m_vpv[0] = (self.m_vpv[0] + gw.m_vpv[0]) / 2
      igw.m_vpv[1] = (self.m_vpv[1] + gw.m_vpv[1]) / 2
      igw.m_ipv[0] = (self.m_ipv[0] + gw.m_ipv[0]) / 2
      igw.m_ipv[1] = (self.m_ipv[1] + gw.m_ipv[1]) / 2
      igw.m_vac[0] = (self.m_vac[0] + gw.m_vac[0]) / 2
      igw.m_vac[1] = (self.m_vac[1] + gw.m_vac[1]) / 2
      igw.m_vac[2] = (self.m_vac[2] + gw.m_vac[2]) / 2
      igw.m_iac[0] = (self.m_iac[0] + gw.m_iac[0]) / 2
      igw.m_iac[1] = (self.m_iac[1] + gw.m_iac[1]) / 2
      igw.m_iac[2] = (self.m_iac[2] + gw.m_iac[2]) / 2
      igw.m_fac[0] = (self.m_fac[0] + gw.m_fac[0]) / 2
      igw.m_fac[1] = (self.m_fac[1] + gw.m_fac[1]) / 2
      igw.m_fac[2] = (self.m_fac[2] + gw.m_fac[2]) / 2
      igw.m_pgrid = (self.m_pgrid + gw.m_pgrid) / 2
      igw.m_eday = (self.m_eday + gw.m_eday) / 2
      igw.m_etotal = (self.m_etotal + gw.m_etotal) / 2
      igw.m_htotal = (self.m_htotal + gw.m_htotal) / 2
      igw.m_temperature = (self.m_temperature + gw.m_temperature) / 2
      igw.m_efficiency = (self.m_efficiency + gw.m_efficiency) / 2
      
      return igw
      
   def get_vpv0( gw):
      return gw.m_vpv[0]
   def get_vpv1( gw):
      return gw.m_vpv[1]
   def get_ipv0( gw):
      return gw.m_ipv[0]
   def get_ipv1( gw):
      return gw.m_ipv[1]
   def get_vac0( gw):
      return gw.m_vac[0]
   def get_vac1( gw):
      return gw.m_vac[1]
   def get_vac2( gw):
      return gw.m_vac[2]
   def get_iac0( gw):
      return gw.m_iac[0]
   def get_iac1( gw):
      return gw.m_iac[1]
   def get_iac2( gw):
      return gw.m_iac[2]
   def get_fac0( gw):
      return gw.m_fac[0]
   def get_fac1( gw):
      return gw.m_fac[1]
   def get_fac2( gw):
      return gw.m_fac[2]
   def get_pgrid( gw):
      return gw.m_pgrid
   def get_eday( gw):
      return gw.m_eday
   def get_etotal( gw):
      return gw.m_etotal
   def get_htotal( gw):
      return gw.m_htotal
   def get_temperature( gw):
      return gw.m_temperature
   def get_efficiency( gw):
      return gw.m_efficiency
   
   
   
   
