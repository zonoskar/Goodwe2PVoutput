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
         self.parse_data( urlData)
      except Exception, arg:
         print "Filter data Error: " + str(arg)


   #--------------------------------------------------------------------------
   def parse_data( self, response):
   #Parses the URL data. This will select the correct table from the 
   #URL data and strip all units from the data strings ready to be 
   #converted to float or integers.
   #
      # Select from the HTTP data the table row with DG_Item
      title = response[response.find('<title>')+7:response.find('</title>')]
      table = response[response.find('var pw_info ='):response.find('var pw_id')]
      inverter = table[table.find('inverter'):]
      inverter = inverter[12:inverter.find('next_device')]
      inverter = inverter.replace('"', '')
      values = inverter.split(',')
      data = {}
      
      # Convert the list into a dictionary for easy access.
      for f in values:
         k = f[:f.find(":")]
         v = f[f.find(":")+1:]
         data[k] = v
         
      # Get the data from the dictionary
      try:
         self.m_sample.set_line( 1)
         if data['status'] == "1":
            self.m_sample.set_inverter_status( 'Normal')
         else:
            self.m_sample.set_inverter_status( 'Error')
         
         self.m_sample.set_inverter_sn( data['sn'])
         self.m_sample.set_description( "last refresh: " + data['last_refresh_time'])
         self.m_sample.set_error( data['warning'])

         self.m_sample.set_pgrid( self._convert_line_to_float( data['pac']))
         self.m_sample.set_eday( self._convert_line_to_float( data['eDay']))
         self.m_sample.set_etotal( self._convert_line_to_float( data['eTotal']))
         self.m_sample.set_htotal( self._convert_line_to_float( data['hTotal']))
         self.m_sample.set_temperature( self._convert_line_to_float(data['tempperature']))
        
         self.m_sample.set_vpv( 0, self._convert_line_to_float(data['vpv1']))
         self.m_sample.set_vpv( 1, self._convert_line_to_float(data['vpv2']))
         self.m_sample.set_ipv( 0, self._convert_line_to_float(data['ipv1']))
         self.m_sample.set_ipv( 1, self._convert_line_to_float(data['ipv2']))

         self.m_sample.set_vac( 0, self._convert_line_to_float(data['vac1']))
         self.m_sample.set_vac( 1, self._convert_line_to_float(data['vac2']))
         self.m_sample.set_vac( 2, self._convert_line_to_float(data['vac3']))
         self.m_sample.set_iac( 0, self._convert_line_to_float(data['iac1']))
         self.m_sample.set_iac( 1, self._convert_line_to_float(data['iac2']))
         self.m_sample.set_iac( 2, self._convert_line_to_float(data['iac3']))
         self.m_sample.set_fac( 0, self._convert_line_to_float(data['fac1']))
         self.m_sample.set_fac( 1, self._convert_line_to_float(data['fac2']))
         self.m_sample.set_fac( 2, self._convert_line_to_float(data['fac3']))

         self.m_sample.set_consume_day( 0.0)
         self.m_sample.set_consume_total( 0.0)

         # Calculate efficiency (PowerAC / powerDC)
         try:
            ppv = ((self.m_sample.get_vpv(0) * self.m_sample.get_ipv(0)) + (self.m_sample.get_vpv(1) * self.m_sample.get_ipv(1)))
            if ppv > 0.0:
               self.m_sample.set_efficiency( self.m_sample.get_pgrid() / ppv)
         except Exception, arg:
            print "Calculate Efficiency Error: " + str(arg)
            self.m_sample.set_efficiency( 0.0)
         except:
            pass
      except Exception, ex:
         raise IOError("Data from Goodwe portal not correct: " + str(ex))


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
      return self.m_sample.is_online()
      

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
