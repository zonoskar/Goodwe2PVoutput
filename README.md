# Goodwe2PVoutput
Python modules needed (most of them are standard, the install command is given when non-standard):
- time
- copy
- usb (pip install pyusb)
- array
- copy
- time
- zlib
- enum
- numpy (pip install numpy)
- requests (pip install requests)
- serial (pip install pyserial)


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
is not important). An example file is found in the data directory in the GIT repository:

goodwe_system_id: 'Your Goodwe system ID'

goodwe_user_id: 'Your username on goodwe-power.com'

goodwe_server: 'The Goodwe server you are using, eu, au or www

goodwe_passwd: 'This is optional. If supplied, the script won't ask for the password at startup. But be ware it is stored in plain text, so make sure only you are able to read the file. (perform 'chmod 600 <config file>' on the config file).

pvoutput_system_id: 'Your PVOutput system ID'

pvoutput_api: 'Your PVOutput API key'

csv_dir: 'Path where the CSV files are stored. This path must exist and be readable.'

spline_fit: 'True or False. When True, the new spline fit smooths the data sent to PVoutput'

input_source: 'URL or USB. When USB, the data will be read from the USB port of the inverter, but this option doesn't work yet. When URL, it scrapes data from the Goodwe-power.com site. This is the preferred option that does work.'

The character '#' can be used to denote comments, from this character to the
end of the line will be ignored. An example is provided in the data direcotry.

Make sure the file is readable by everyone.

For USB access, change the USB permission according to this site: http://ask.xmodulo.com/change-usb-device-permission-linux.html


##############################################################
## USB mode is in development, but should work
##############################################################
To enable USB mode, attach a USB cable and change the input_source to USB. However, on my inverter, this only works after the inverter has started. I split the USB cable and added a simple 2-way relais between. This USB relais is switched using the GPIO pin specified in the corresponding setting. See the supplied default config file for more info. This is all alpha software, so use at your own risk.



Start:
python -m Goodwe2PVoutput
