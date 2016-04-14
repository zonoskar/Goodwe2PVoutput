  
class goodweData :

   #--------------------------------------------------------------------------
   def __init__( self, urlData):
   #Initialization of the goodweData class. All data members are set
   #to default values. Then the urlData is filtered and parsed
      self.m_line = ''
      self.m_inverter_sn = ''
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
      self.m_vpv1 = 0.0
      self.m_vpv2 = 0.0
      self.m_ipv1 = 0.0
      self.m_ipv2 = 0.0
      self.m_vac1 = 0.0
      self.m_vac2 = 0.0
      self.m_vac3 = 0.0
      self.m_iac1 = 0.0
      self.m_iac2 = 0.0
      self.m_iac3 = 0.0
      self.m_fac1 = 0.0
      self.m_fac2 = 0.0
      self.m_fac3 = 0.0
      self.m_loadV = 0.0
      self.m_loadA = 0.0
      self.m_loadW = 0.0
      self.m_consume_day = 0.0
      self.m_consume_total = 0.0
      self.m_efficiency = 0.0
      
      filteredData = self.filter_data( urlData)
      self.parse_data( filteredData)

   #--------------------------------------------------------------------------
   def parse_data( self, filteredData):
   #Parses the filtered data. This will yield nice and usable
   #data member values.
   #
      self.m_line = filteredData[0]
      self.m_inverter_sn = filteredData[1]
      self.m_inverter_status = filteredData[2]
      self.m_error = filteredData[7]

      #Values that I'm not using (or don't know what they are
      self.m_vbattery = filteredData[14].replace(' ', '') # 0.0/0.0V
      self.m_ibattery = filteredData[15].replace(' ', '') # 0.0/0.0A
      self.m_soc = filteredData[16].replace(' ', '') # 0/0%

      # Only select 1 significant digit after .
      try:
         self.m_pgrid = float(filteredData[3].replace('W', ''))
         self.m_eday = float(filteredData[4].replace('kWh', ''))
         self.m_etotal = float(filteredData[5].replace('kWh', ''))
         self.m_htotal = float(filteredData[6].replace('h', ''))
         self.m_temperature = float(filteredData[13][0:filteredData[13].find('.')+2])

         #multi line values, separated by '/'
         v = filteredData[8].split('/')
         if len(v) > 1:
            self.m_vpv1 = float(v[0].replace('V', ''))
            self.m_vpv2 = float(v[1].replace('V', ''))

         i = filteredData[9].split('/')
         if len(i) > 1:
            self.m_ipv1 = float(i[0].replace('A', ''))
            self.m_ipv2 = float(i[1].replace('A', ''))
      
         v = filteredData[10].split('/')
         if len(v) > 1:
            self.m_vac1 = float(v[0].replace('V', ''))
            self.m_vac2 = float(v[1].replace('V', ''))
            self.m_vac3 = float(v[2].replace('V', ''))
         
         i = filteredData[11].split('/')
         if len(i) > 1:
            self.m_iac1 = float(i[0].replace('A', ''))
            self.m_iac2 = float(i[1].replace('A', ''))
            self.m_iac3 = float(i[2].replace('A', ''))
         
         f = filteredData[11].split('/')
         if len(i) > 1:
            self.m_fac1 = float(f[0].replace('Hz', ''))
            self.m_fac2 = float(f[1].replace('Hz', ''))
            self.m_fac3 = float(f[2].replace('Hz', ''))

         load = filteredData[17].split('/')
         if len(load) > 1:
            self.m_loadV = float(load[0].replace('V', ''))
            self.m_loadA = float(load[1].replace('A', ''))
            self.m_loadW = float(load[2].replace('KW', ''))

         self.m_consume_day = float(filteredData[18].replace('kWh', ''))
         self.m_consume_total = float(filteredData[19].replace('kWh', ''))
      except(ValueError):
         #use default values
         pass

      # Calculate efficiency (PowerAC / powerDC)
      ppv = ((self.m_vpv1 * self.m_ipv1) + (self.m_vpv2 * self.m_ipv2))
      if ppv > 0.0:
         self.m_efficiency = self.m_pgrid / ppv


   #--------------------------------------------------------------------------
   def filter_data( self, response):
   #Filters the URL data. This will select the correct table from the 
   #URL data and strip all units from the data strings ready to be 
   #converted to float or integers.
   #
      # Select from the HTTP data the table row with DG_Item
      table = response[response.find('<tr class="DG_Item">')+20:]
      table = table[:table.find('</tr>')]
      table = table.replace(' ', '')
      
      # Split the table row in columns using the <td> HTTP tag
      r = table.split('<td>')
      l = []
      for line in r:
         if '</td>' in line:
            line=line.replace('</td>', '')
            line=line.replace('\r\n', '')
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
            l.append(line)
      return l
   

   #--------------------------------------------------------------------------
   def to_short_string( self):
   #Creates a string repesentation of the class
   #
      return "S/N: " + str(self.m_inverter_sn) + " P:" + str(self.m_pgrid) + " E:" + str(self.m_eday) + " V:" + str(self.m_vpv1+self.m_vpv2)


   #--------------------------------------------------------------------------
   def to_string( self):
   #Creates a string repesentation of the class
   #
      return self.to_csv_string().replace(',', '')


   #--------------------------------------------------------------------------
   def to_csv_string( self):
   #Creates a string repesentation of the class, separated by ','.
   #
      return str(self.m_line) + ", " + str(self.m_inverter_sn) + ", " + str(self.m_inverter_status) + ", " + str(self.m_pgrid) + ", " + str(self.m_eday) + ", " + str(self.m_etotal) + ", " + str(self.m_htotal) + ", " + str(self.m_error) + ", " + str(self.m_vpv1) + ", " + str(self.m_vpv2) + ", " + str(self.m_ipv1) + ", " + str(self.m_ipv2) + ", " + str(self.m_vac1) + ", " + str(self.m_vac2) + ", " + str(self.m_vac3) + ", " + str(self.m_iac1) + ", " + str(self.m_iac2) + ", " + str(self.m_iac3) + ", " + str(self.m_fac1) + ", " + str(self.m_fac2) + ", " + str(self.m_fac3) + ", " + str(self.m_temperature) + ", " + str(self.m_vbattery) + ", " + str(self.m_ibattery) + ", " + str(self.m_soc) + ", " + str(self.m_loadV) + ", " + str(self.m_loadA) + ", " + str(self.m_loadW) + ", " + str(self.m_consume_day) + ", " + str(self.m_consume_total) + ", " + str(self.m_efficiency)


   #--------------------------------------------------------------------------
   def get_csv_header( self):
   #Returns the CSV header format string.
   #
      return "Line, Inverter_SN, Inverter_status, Pgrid, Eday, Etotal, Htotal, Error, Vpv1, Vpv2, Ipv1, Ipv2, Vac1, Vac2, Vac3, Iac1, Iac2, Iac3, Fac1, Fac2, Fac3, Temperature, Vbattery, Ibattery, SOC, Vload, Iload, Pload, Consume_day, Consume_total, Efficiency"


   #--------------------------------------------------------------------------
   def is_online( self):
   #TRUE when the GoodWe inverter returns the correct status
   #
      return (self.m_inverter_status == 'Normal') and (abs(self.m_vpv1) > 0.05) and (abs(self.m_vpv2) > 0.05)
      

   #--------------------------------------------------------------------------
   def is_identical( self, gw):
   #Compares select data members to determine if two instances of the
   #goodweData class are identical
   #
      eps = 0.05
      if not gw:
         return False
         
      if (abs(self.m_vpv1 - gw.m_vpv1) < eps) and \
         (abs(self.m_vpv2 - gw.m_vpv2) < eps) and \
         (abs(self.m_ipv1 - gw.m_ipv1) < eps) and \
         (abs(self.m_ipv2 - gw.m_ipv2) < eps) and \
         (abs(self.m_pgrid - gw.m_pgrid) < eps) and \
         (abs(self.m_vac1 - gw.m_vac1) < eps) and \
         (abs(self.m_vac2 - gw.m_vac2) < eps) and \
         (abs(self.m_vac3 - gw.m_vac3) < eps) and \
         (abs(self.m_iac1 - gw.m_iac1) < eps) and \
         (abs(self.m_iac2 - gw.m_iac2) < eps) and \
         (abs(self.m_iac3 - gw.m_iac3) < eps) and \
         (abs(self.m_fac1 - gw.m_fac1) < eps) and \
         (abs(self.m_fac2 - gw.m_fac2) < eps) and \
         (abs(self.m_fac3 - gw.m_fac3) < eps) :
         return True
         
      return False      


   #--------------------------------------------------------------------------
   def interpolate( self, gw):
   #Interpolates two goodweData class instances by using linear 
   #interpolation. This will yield a nicer graph in PVoutput.org
   #
      igw = gw
      
      igw.m_vpv1 = (self.m_vpv1 + gw.m_vpv1) / 2
      igw.m_vpv2 = (self.m_vpv2 + gw.m_vpv2) / 2
      igw.m_ipv1 = (self.m_ipv1 + gw.m_ipv1) / 2
      igw.m_ipv2 = (self.m_ipv2 + gw.m_ipv2) / 2
      igw.m_vac1 = (self.m_vac1 + gw.m_vac1) / 2
      igw.m_vac2 = (self.m_vac2 + gw.m_vac2) / 2
      igw.m_vac3 = (self.m_vac3 + gw.m_vac3) / 2
      igw.m_iac1 = (self.m_iac1 + gw.m_iac1) / 2
      igw.m_iac2 = (self.m_iac2 + gw.m_iac2) / 2
      igw.m_iac3 = (self.m_iac3 + gw.m_iac3) / 2
      igw.m_fac1 = (self.m_fac1 + gw.m_fac1) / 2
      igw.m_fac2 = (self.m_fac2 + gw.m_fac2) / 2
      igw.m_fac3 = (self.m_fac3 + gw.m_fac3) / 2
      igw.m_pgrid = (self.m_pgrid + gw.m_pgrid) / 2
      igw.m_eday = (self.m_eday + gw.m_eday) / 2
      igw.m_etotal = (self.m_etotal + gw.m_etotal) / 2
      igw.m_htotal = (self.m_htotal + gw.m_htotal) / 2
      igw.m_temperature = (self.m_temperature + gw.m_temperature) / 2
      
      return igw
      
      
      
      
   
   
   
   
