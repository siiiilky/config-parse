import functions

####### Examples
#
# Get hostname of device and create a csv called hostname.csv
# containing CDP neighbours and interfaces.
#
# Configuration to be done in config.py
#
# Device type (cisco_ios, cisco_nxos)
deviceType = 'cisco_ios'
# Connect to the device
connection = functions.connect('10.100.100.52', deviceType)
# Retrieve hostname
hostname = functions.get_hostname(connection)
# Create CSV containing CDP information
functions.cdp_to_csv(connection, hostname, deviceType)
# Create text file containing switch CDP output
functions.get_cdp(connection, hostname)
# Run and adhoc command
functions.get_adhoc(connection, hostname, "show ver")
# close SSH connection
connection.disconnect()





