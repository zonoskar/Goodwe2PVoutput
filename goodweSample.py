import copy


class goodweSample :

   #--------------------------------------------------------------------------
   def __init__( self):
   #Initialization of the goodweSample class. All data members are set
   #to default values. Then the urlData is filtered and parsed
      self.m_line = ''
      self.m_inverter_sn = ''
      self.m_description = ''
      self.m_inverter_status = 'offline'
      self.m_error = ''
      self.m_vbattery = ''
      self.m_ibattery = ''
      self.m_soc = ''
      self.m_pgrid = 0.0
      self.m_eday = 0.0
      self.m_eday_calc = 0.0
      self.m_etotal = 0.0
      self.m_htotal = 0.0
      self.m_temperature = 0.0
      self.m_vload = 0.0
      self.m_iload = 0.0
      self.m_pload = 0.0

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
   def to_calc_string( self):
   #Creates a string repesentation of the class
   #
      return " P:" + str(self.m_pgrid) + " Ec:" + str(self.m_eday_calc) + " E:" + str(self.m_eday) + " V:" + str(self.m_vpv[0]+self.m_vpv[1])

   #--------------------------------------------------------------------------
   def to_short_string( self):
   #Creates a string repesentation of the class
   #
      return " P:" + str(self.m_pgrid) + " E:" + str(self.m_eday) + " V:" + str(self.m_vpv[0]+self.m_vpv[1]) + " T:" + str(self.m_temperature)


   #--------------------------------------------------------------------------
   def to_string( self):
   #Creates a string repesentation of the class
   #
      return self.to_csv_string().replace(',', '')


   #--------------------------------------------------------------------------
   def get_csv_header( self):
   #Returns the CSV header format string.
   #
      return "Date, Time, Line, Inverter_SN, Inverter_status, Pgrid, Eday, Etotal, Htotal, Error, Vpv1, Vpv2, Ipv1, Ipv2, Vac1, Vac2, Vac3, Iac1, Iac2, Iac3, Fac1, Fac2, Fac3, Temperature, Vbattery, Ibattery, SOC, Vload, Iload, Pload, Consume_day, Consume_total, Efficiency"


   #--------------------------------------------------------------------------
   def to_csv_string( self):
   #Creates a string repesentation of the class, separated by ','.
   #
      return str(self.m_line) + ", " + str(self.m_inverter_sn) + ", " + str(self.m_description) + ", " + str(self.m_inverter_status) + ", " + str(self.m_pgrid) + ", " + str(self.m_eday) + ", " + str(self.m_etotal) + ", " + str(self.m_htotal) + ", " + str(self.m_error) + ", " + str(self.m_vpv[0]) + ", " + str(self.m_vpv[1]) + ", " + str(self.m_ipv[0]) + ", " + str(self.m_ipv[1]) + ", " + str(self.m_vac[0]) + ", " + str(self.m_vac[1]) + ", " + str(self.m_vac[2]) + ", " + str(self.m_iac[0]) + ", " + str(self.m_iac[1]) + ", " + str(self.m_iac[2]) + ", " + str(self.m_fac[0]) + ", " + str(self.m_fac[1]) + ", " + str(self.m_fac[2]) + ", " + str(self.m_temperature) + ", " + str(self.m_consume_day) + ", " + str(self.m_consume_total) + ", " + str(self.m_efficiency)


   #--------------------------------------------------------------------------
   def to_detailed_string( self):
   #Creates a detailed string repesentation of the class
   #
      s = 'Goodwe sample for inverter '
      s = s + "S/N:     " + str(self.m_inverter_sn) + "\n"
      s = s + "Desc:    " + str(self.m_description) + "\n"
      s = s + "Status:  " + str(self.m_inverter_status) + "\n"
      s = s + "Pgrid:   " + str(self.m_pgrid) + "\n"
      s = s + "Eday:    " + str(self.m_eday) + "\n"
      s = s + "EdayCalc:" + str(self.m_eday_calc) + "\n"
      s = s + "Etotal:  " + str(self.m_etotal) + "\n"
      s = s + "Htotal:  " + str(self.m_htotal) + "\n"
      s = s + "Error:   " + str(self.m_error) + "\n"
      s = s + "Vpv0:  " + str(self.m_vpv[0]) + "\n"
      s = s + "Vpv1:  " + str(self.m_vpv[1]) + "\n"
      s = s + "Ipv0:  " + str(self.m_ipv[0]) + "\n"
      s = s + "Ipv1:  " + str(self.m_ipv[1]) + "\n"
      s = s + "Vac0:  " + str(self.m_vac[0]) + "\n"
      s = s + "Vac1:  " + str(self.m_vac[1]) + "\n"
      s = s + "Vac2:  " + str(self.m_vac[2]) + "\n"
      s = s + "Iac0:  " + str(self.m_iac[0]) + "\n"
      s = s + "Iac1:  " + str(self.m_iac[1]) + "\n"
      s = s + "Iac2:  " + str(self.m_iac[2]) + "\n"
      s = s + "Fac0:  " + str(self.m_fac[0]) + "\n"
      s = s + "Fac1:  " + str(self.m_fac[1]) + "\n"
      s = s + "Fac2:  " + str(self.m_fac[2]) + "\n"
      s = s + "Temp:  " + str(self.m_temperature) + "\n"
      s = s + "Vbat:  " + str(self.m_vbattery) + "\n"
      s = s + "Ibat:  " + str(self.m_ibattery) + "\n"
      s = s + "SOC:   " + str(self.m_soc) + "\n"
      s = s + "Vload: " + str(self.m_vload) + "\n"
      s = s + "Iload: " + str(self.m_iload) + "\n"
      s = s + "Pload: " + str(self.m_pload) + "\n"
      s = s + "Cday:  " + str(self.m_consume_day) + "\n"
      s = s + "Ctot:  " + str(self.m_consume_total) + "\n"
      s = s + "Eff:   " + str(self.m_efficiency)

      return s


   #--------------------------------------------------------------------------
   def is_identical( self, gw):
   #Compares select data members to determine if two instances of the
   #goodweSample class are identical
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
   def interpolate( self, sample):
   #Interpolates two goodweSample class instances by using linear 
   #interpolation. This will yield a nicer graph in PVoutput.org
   #
      isample = copy.deepcopy(sample)
      
      isample.set_vpv(0, (self.get_vpv(0) + sample.get_vpv(0)) / 2)
      isample.set_vpv(1, (self.get_vpv(1) + sample.get_vpv(1)) / 2)
      isample.set_ipv(0, (self.get_ipv(0) + sample.get_ipv(0)) / 2)
      isample.set_ipv(1, (self.get_ipv(1) + sample.get_ipv(1)) / 2)
      isample.set_vac(0, (self.get_vac(0) + sample.get_vac(0)) / 2)
      isample.set_vac(1, (self.get_vac(1) + sample.get_vac(1)) / 2)
      isample.set_vac(2, (self.get_vac(2) + sample.get_vac(2)) / 2)
      isample.set_iac(0, (self.get_iac(0) + sample.get_iac(0)) / 2)
      isample.set_iac(1, (self.get_iac(1) + sample.get_iac(1)) / 2)
      isample.set_iac(2, (self.get_iac(2) + sample.get_iac(2)) / 2)
      isample.set_fac(0, (self.get_fac(0) + sample.get_fac(0)) / 2)
      isample.set_fac(1, (self.get_fac(1) + sample.get_fac(1)) / 2)
      isample.set_fac(2, (self.get_fac(2) + sample.get_fac(2)) / 2)
      isample.set_pgrid( (self.get_pgrid() + sample.get_pgrid()) / 2)
      isample.set_eday( (self.get_eday() + sample.get_eday()) / 2)
      isample.set_eday_calc( (self.get_eday_calc() + sample.get_eday_calc()) / 2)
      isample.set_etotal( (self.get_etotal() + sample.get_etotal()) / 2)
      isample.set_htotal( (self.get_htotal() + sample.get_htotal()) / 2)
      isample.set_temperature( (self.get_temperature() + sample.get_temperature()) / 2)
      isample.set_efficiency( (self.get_efficiency() + sample.get_efficiency()) / 2)
      
      return isample

   #--------------------------------------------------------------------------
   def is_online( self):
   #
      return ((self.is_inverter_status('Normal')) and (abs(self.get_vpv(0)+self.get_vpv(1)) > 0.01))
            

   #--------------------------------------------------------------------------
   def is_inverter_status( self, status):
       return status == self.m_inverter_status

             
   #--------------------------------------------------------------------------
   def get_vpv( self, i):
      return self.m_vpv[i]
   def get_vpv0( self):
      return self.m_vpv[0]
   def get_vpv1( self):
      return self.m_vpv[1]

   def get_ipv( self, i):
      return self.m_ipv[i]
   def get_ipv0( self):
      return self.m_ipv[0]
   def get_ipv1( self):
      return self.m_ipv[1]

   def get_vac( self, i):
      return self.m_vac[i]
   def get_vac0( self):
      return self.m_vac[0]
   def get_vac1( self):
      return self.m_vac[1]
   def get_vac2( self):
      return self.m_vac[2]

   def get_iac( self, i):
      return self.m_iac[i]
   def get_iac0( self):
      return self.m_iac[0]
   def get_iac1( self):
      return self.m_iac[1]
   def get_iac2( self):
      return self.m_iac[2]

   def get_fac( self, i):
      return self.m_fac[i]
   def get_fac0( self):
      return self.m_fac[0]
   def get_fac1( self):
      return self.m_fac[1]
   def get_fac2( self):
      return self.m_fac[2]

   def get_pgrid( self):
      return self.m_pgrid

   def get_eday( self):
      return self.m_eday
   def get_eday_calc( self):
      return self.m_eday_calc

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
      return self.m_vload
   
   def get_consume_day( self):
      return self.m_consume_day
   
   def get_consume_total( self):
      return self.m_consume_total
   
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
   def set_eday_calc( self, val):
      self.m_eday_calc = val
   def add_eday_calc( self, val, seconds):
      self.m_eday_calc += val * (seconds / 3600.0)

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
      self.m_vload = val
   
   def set_consume_day( self, val):
      self.m_consume_day = val
   
   def set_consume_total( self, val):
      self.m_consume_total = val
   
   def set_inverter_sn( self, val):
      self.m_inverter_sn = val
   
   
   
   
#---------------- End of file ------------------------------------------------
