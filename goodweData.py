  
class goodweData :

   #--------------------------------------------------------------------------
   def __init__( self, url):

      l = self.filter_data( url)

      self.m_line = l[0]
      self.m_inverter_sn = l[1]
      self.m_inverter_status = l[2]
      try:
         self.m_pgrid = float(l[3].replace('W', ''))
      except(ValueError):
         self.m_pgrid = 0.0
      try:
         self.m_eday = float(l[4].replace('kWh', ''))
      except(ValueError):
         self.m_eday = 0.0
      self.m_etotal = float(l[5].replace('kWh', ''))
      self.m_htotal = float(l[6].replace('h', ''))
      self.m_error = l[7]
      v = l[8].split('/')
      if len(v) > 1:
         self.m_vpv1 = float(v[0].replace('V', ''))
         self.m_vpv2 = float(v[1].replace('V', ''))
      else:
         self.m_vpv1 = 0.0
         self.m_vpv2 = 0.0

      i = l[9].split('/')
      if len(i) > 1:
         self.m_ipv1 = float(i[0].replace('A', ''))
         self.m_ipv2 = float(i[1].replace('A', ''))
      else:
         self.m_ipv1 = 0.0
         self.m_ipv2 = 0.0
      
      v = l[10].split('/')
      if len(v) > 1:
         self.m_vac1 = float(v[0].replace('V', ''))
         self.m_vac2 = float(v[1].replace('V', ''))
         self.m_vac3 = float(v[2].replace('V', ''))
      else:
         self.m_vac1 = 0.0
         self.m_vac2 = 0.0
         self.m_vac3 = 0.0
	 
      i = l[11].split('/')
      if len(i) > 1:
         self.m_iac1 = float(i[0].replace('A', ''))
         self.m_iac2 = float(i[1].replace('A', ''))
         self.m_iac3 = float(i[2].replace('A', ''))
      else:
         self.m_iac1 = 0.0
         self.m_iac2 = 0.0
         self.m_iac3 = 0.0
	 
      f = l[11].split('/')
      if len(i) > 1:
         self.m_fac1 = float(f[0].replace('Hz', ''))
         self.m_fac2 = float(f[1].replace('Hz', ''))
         self.m_fac3 = float(f[2].replace('Hz', ''))
      else:
         self.m_fac1 = 0.0
         self.m_fac2 = 0.0
         self.m_fac3 = 0.0
      # Only select 1 significant digit after .
      try:
         self.m_temperature = float(l[13][0:l[13].find('.')+2])
      except(ValueError):
         self.m_temperature = 0.0
      self.m_vbattery = l[14].replace(' ', '') # 0.0/0.0V
      self.m_ibattery = l[15].replace(' ', '') # 0.0/0.0A
      self.m_soc = l[16].replace(' ', '') # 0/0%
      load = l[17].split('/')
      if len(load) > 1:
         self.m_loadV = float(load[0].replace('V', ''))
         self.m_loadA = float(load[1].replace('A', ''))
         self.m_loadW = float(load[2].replace('KW', ''))
      else:
         self.m_loadV = 0.0
         self.m_loadA = 0.0
         self.m_loadW = 0.0
      
      try:
         self.m_consume_day = float(l[18].replace('kWh', ''))
      except(ValueError):
         self.m_consume_day = 0.0
      self.m_consume_total = float(l[19].replace('kWh', ''))
      ppv = ((self.m_vpv1 * self.m_ipv1) + (self.m_vpv2 * self.m_ipv2))
      if ppv > 0.0:
         self.m_efficiency = self.m_pgrid / ppv
      else:
         self.m_efficiency = 0.0
	 
   
   #--------------------------------------------------------------------------
   def filter_data( self, response):
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
   def to_string( self):
      return self.to_csv_string().replace(',', '')

   #--------------------------------------------------------------------------
   def to_csv_string( self):
      return str(self.m_line) + ", " + str(self.m_inverter_sn) + ", " + str(self.m_inverter_status) + ", " + str(self.m_pgrid) + ", " + str(self.m_eday) + ", " + str(self.m_etotal) + ", " + str(self.m_htotal) + ", " + str(self.m_error) + ", " + str(self.m_vpv1) + ", " + str(self.m_vpv2) + ", " + str(self.m_ipv1) + ", " + str(self.m_ipv2) + ", " + str(self.m_vac1) + ", " + str(self.m_vac2) + ", " + str(self.m_vac3) + ", " + str(self.m_iac1) + ", " + str(self.m_iac2) + ", " + str(self.m_iac3) + ", " + str(self.m_fac1) + ", " + str(self.m_fac2) + ", " + str(self.m_fac3) + ", " + str(self.m_temperature) + ", " + str(self.m_vbattery) + ", " + str(self.m_ibattery) + ", " + str(self.m_soc) + ", " + str(self.m_loadV) + ", " + str(self.m_loadA) + ", " + str(self.m_loadW) + ", " + str(self.m_consume_day) + ", " + str(self.m_consume_total) + ", " + str(self.m_efficiency)


   #--------------------------------------------------------------------------
   def get_csv_header( self):
      return "Line, Inverter_SN, Inverter_status, Pgrid, Eday, Etotal, Htotal, Error, Vpv1, Vpv2, Ipv1, Ipv2, Vac1, Vac2, Vac3, Iac1, Iac2, Iac3, Fac1, Fac2, Fac3, Temperature, Vbattery, Ibattery, SOC, Vload, Iload, Pload, Consume_day, Consume_total, Efficiency"


   #--------------------------------------------------------------------------
   def is_online( self):
      return self.m_inverter_status == 'Normal'
      

   #--------------------------------------------------------------------------
   def is_identical( self, gw):
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
      
      print "Interpolated: " + igw.to_string()
      return igw
      
      
      
      
   
   
   
   
