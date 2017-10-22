  
class goodweSample :

   #--------------------------------------------------------------------------
   def __init__( self):
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
   def is_inverter_status( self, status):
       return status == self.m_inverter_status

             
   #--------------------------------------------------------------------------
   def get_vpv( self, i):
      return self.m_vpv[i]

   def get_ipv( self, i):
      return self.m_ipv[i]

   def get_vac( self, i):
      return self.m_vac[i]

   def get_iac( self, i):
      return self.m_iac[i]

   def get_fac( self, i):
      return self.m_fac[i]

   def get_pgrid( self):
      return self.m_pgrid

   def get_eday( self):
      return self.m_eday

   def get_etotal( self):
      return self.m_etotal

   def get_htotal( self):
      return self.m_htotal

   def get_temperature( self):
      return self.m_temperature

   def get_efficiency( self):
      return self.m_efficiency
   
   def get_line( self):
      return self.m_line
   
   def get_inverter_status( self):
      return self.m_inverter_status
   
   def get_inverter_sn( self):
      return self.m_inverter_sn
   
   def get_description( self):
      return self.m_description
   
   def get_error( self):
      return self.m_error
   
   def get_vbattery( self):
      return self.m_vbattery
   
   def get_ibattery( self):
      return self.m_ibattery
   
   def get_soc( self):
      return self.m_soc
   
   def get_load( self):
      return self.m_load
   
   def get_consume_day( self):
      return self.m_consume_day
   
   def get_consume_total( self):
      return self.m_consume_total
   
   def is_online( self):
      return self.is_inverter_status( 'Normal')   
   
   #--------------------------------------------------------------------------
   def set_vpv( self, i, val):
      self.m_vpv[i] = val

   def set_ipv( self, i, val):
      self.m_ipv[i] = val

   def set_vac( self, i, val):
      self.m_vac[i] = val

   def set_iac( self, i, val):
      self.m_iac[i] = val

   def set_fac( self, i, val):
      self.m_fac[i] = val

   def set_pgrid( self, val):
      self.m_pgrid = val

   def set_eday( self, val):
      self.m_eday = val

   def set_etotal( self, val):
      self.m_etotal = val

   def set_htotal( self, val):
      self.m_htotal = val

   def set_temperature( self, val):
      self.m_temperature = val

   def set_efficiency( self, val):
      self.m_efficiency = val

   def set_line( self, val):
      self.m_line = val
   
   def set_inverter_status( self, val):
      self.m_inverter_status = val
   
   def set_inverter_sn( self, val):
      self.m_inverter_sn = val
   
   def set_description( self, val):
      self.m_description = val
   
   def set_error( self, val):
      self.m_error = val
   
   def set_vbattery( self, val):
      self.m_vbattery = val
   
   def set_ibattery( self, val):
      self.m_ibattery = val
   
   def set_soc( self, val):
      self.m_soc = val
   
   def set_load( self, val):
      self.m_load = val
   
   def set_consume_day( self, val):
      self.m_consume_day = val
   
   def set_consume_total( self, val):
      self.m_consume_total = val
   
   
   
   
