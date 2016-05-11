# Goodwe2PVoutput
Script to upload Goodwe power invertor data to PVoutput website

Extract zip file to a directory named Goodwe2PVoutput (this is later used with the "python -m" command). Make sure this directory is in the $PATH variable.

Usage:

Create a configuration file in your home directory indicated by the $HOME
environment variable. This file must contain the following information (replace
text between <> by your information, the order is not important):

goodwe_system_id: <Your Goodwe system ID>
goodwe_user_id: <Your username on goodwe-power.com>
pvoutput_system_id: <Your PVOutput system ID>
pvoutput_api: <Your PVOutput API key>
csv_dir: <Path where the CSV files are stored>

The character '#' can be used to denote comments, from this character to the
end of the line will be ignored.

Make sure the file is readable by everyone.


Start:
python -m Goodwe2PVoutput
