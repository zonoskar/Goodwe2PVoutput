# Goodwe2PVOutput
Script to upload GoodWe power invertor data to [PVOutput](PVOutput.org) website.

## Extended data

Also logs extended data to PVOutput:

| Field | Usage
| ----- | -----
| v7    | Voltage of string 1
| v8    | Voltage of string 2
| v9    | Generated power of string 1 (DC Voltage * DC Current * efficiency)
| v10   | Generated power of string 1 (DC Voltage * DC Current * efficiency)
| v11   | AC voltage (in case of 3 phase inverter, the average of the 3 AC voltages)
| v12   | Efficiency (DC power / AC power)

## Installation

Extract zip file to a directory named Goodwe2PVoutput (this is later used with the `python -m` command). Make sure this directory is in the `$PATH` variable.

## Configuration

Create a configuration file named `.goodwe2pvoutput` in your home directory indicated by the `$HOME` environment variable. This file must contain the following information (replace text between '' by your information, the order is not important):

```
goodwe_system_id:   'Your GoodWe system ID'
goodwe_user_id:     'Your username on goodwe-power.com'
goodwe_password:    'Your password on goodwe-power.com'
pvoutput_system_id: 'Your PVOutput system ID'
pvoutput_api:       'Your PVOutput API key'
csv_dir:            'Path where the CSV files are stored'
```
The password is optional. If not present, the module will ask for it.

The character `#` can be used to denote comments, from this character to the end of the line will be ignored.

## Usage

Start:
```
python -m Goodwe2PVoutput
```

## Systemd service
In case you want to run the script as a Systemd service, you can use the following template:

```
[Unit]
Description=Read GoodWe invertor and upload data to PVOutput

[Service]
Environment="PYTHONPATH=DIR"
ExecStart=/usr/bin/python -u -m Goodwe2PVoutput
User=USER
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace USER with the user which will run the script, and DIR by the directory in which the Goodwe2PVoutput module is located.
