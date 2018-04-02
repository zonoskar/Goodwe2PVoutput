# Goodwe2PVoutput
Script to upload Goodwe power invertor data to PVoutput website. Now also logs extended data to PVoutput:

v7: Voltage of string 1

v8: Voltage of string 2

v9: Generated power of string 1 (DC Voltage * DC Current * efficiency)

v10: Generated power of string 1 (DC Voltage * DC Current * efficiency)

v11: AC voltage (in case of 3 phase inverter, the average of the 3 AC voltages)

v12: Efficiency (DC power / AC power)


Extract zip file to a directory named Goodwe2PVoutput (this is later used with the "python -m" command). Make sure this directory is in the $PATH variable.

Usage:

Create a configuration file named .goodwe2pvoutput in your home directory
indicated by the $HOME environment variable. This file must contain the
following information (replace text between '' by your information, the order 
is not important):

goodwe_system_id: 'Your Goodwe system ID'

goodwe_user_id: 'Your username on goodwe-power.com'

pvoutput_system_id: 'Your PVOutput system ID'

pvoutput_api: 'Your PVOutput API key'

csv_dir: 'Path where the CSV files are stored'

spline_fit: 'True or False. When True, the new spline fit smooths the data sent to PVoutput'

inpout_source: 'URL or USB. When USB, the data will be read from the USB port of the inverter, but this
                option doesn't work yet. When URL, it scrapes data from the Goodwe-power.com site. This is
                the preferred option that does work.'

The character '#' can be used to denote comments, from this character to the
end of the line will be ignored. An example is provided in the data direcotry.

Make sure the file is readable by everyone.


Start:
python -m Goodwe2PVoutput
