import time
  
class csvoutput :

   #--------------------------------------------------------------------------
   def __init__( self, dirname, filename):
      if dirname[:-1] != '/':
         dirname += '/'
      if filename[:-1] != '_':
         filename += '_'
      self.m_filename = dirname + filename

      
   #--------------------------------------------------------------------------
   def write_data( self, pvout, write_header):
      t = time.gmtime()
      openname = self.m_filename + str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2) + ".csv"

      with open(openname, "a") as fs:
         if write_header:
	    fs.write( pvout.get_csv_header() + '\n')
         fs.write( pvout.to_csv_string() + '\n')
     



