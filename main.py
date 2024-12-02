import functions

####### Examples
#
# Get hostname of device and create a csv called hostname.csv
# containing CDP neighbours and interfaces.
#
# Configuration to be done in config.py
#
# Connect to the device
connection = functions.connect('10.100.100.52')
# Device type (cisco_ios, cisco_nxos)
deviceType = functions.get_type(connection)
# Retrieve hostname
hostname = functions.get_hostname(connection)
# Create CSV containing CDP information
functions.cdp_to_csv(connection, hostname, deviceType)
# Create text file containing switch CDP output
functions.get_cdp(connection, hostname)
# Get show run, show run all, and show start
functions.get_configs(connection, hostname)
# Get OSPF infor from device
functions.get_ospf_info(connection, hostname, deviceType)
# Run an adhoc command
functions.get_adhoc(connection, hostname, "show ver")
# Send an interface config command
functions.configure_interface(connection, "g1/3", "no cdp enable")
# Send global config
functions.configure_global(connection, "no banner exec")
# close SSH connection
connection.disconnect()





