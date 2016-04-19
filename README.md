# Goodwe2PVoutput
Script to upload Goodwe power invertor data to PVoutput website

Extract zip file to a directory named Goodwe2PVoutput (this is later used with the "python -m" command)

Usage:

Open file _ _ main _ _.py. Edit the top variables:

   sid = '[your system ID on Goodwe-power.com]'
   
   sys_id = '[your system ID on PVoutput.org]'
   
   api_key = '[Your PVoutput API key (generate one)]'
   
   csv_dir = '[Directory where you want the CSV files]'

Start:
python -m Goodwe2PVoutput
