import logging
import time

class csvoutput :

   #--------------------------------------------------------------------------
   def __init__( self, dirname, filename):
   # This class provides an interface to a CSV fiel output of the measured
   # Goodwe inverter data
   #
      if dirname[:-1] != '/':
         dirname += '/'
      if filename[:-1] != '_':
         filename += '_'
      self.m_filename = dirname + filename
      self.m_write_header = True


   #--------------------------------------------------------------------------
   def write_data( self, pvout):
   # Writes the Goodwe inverted data to a CSV file. The filename is based on
   # the current date and time. When a header is not written, this is done.
   #
      t = time.localtime()
      dateString = str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2) + ',' + str(t.tm_hour).zfill(2) + ':' + str(t.tm_min).zfill(2) + ','
      try:
         openname = self.m_filename + str(t.tm_year).zfill(4) + str(t.tm_mon).zfill(2) + str(t.tm_mday).zfill(2) + ".csv"

         with open(openname, "a") as fs:
            if self.m_write_header:
               fs.write( pvout.get_csv_header() + '\n')
               # next time, no need for a header
	       self.m_write_header = False
            fs.write( dateString + pvout.to_csv_string() + '\n')
      except Exception, arg:
         logging.error("Write CSV data Error: " + str(arg))


   #--------------------------------------------------------------------------
   def reset( self):
   # Resets the CSV writing so the next time a header is written
   #
      self.m_write_header = True


