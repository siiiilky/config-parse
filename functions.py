from netmiko import ConnectHandler
import config
import csv

def connect(ip):
    # establish a connection to the device
    ssh_connection = ConnectHandler(
        device_type="cisco_ios",
        ip=ip,
        username=config.username,
        password=config.password,
        secret=config.secret
    )
    return ssh_connection


def get_hostname(connection):
    # enter enable mode
    connection.enable()
    # execute the show run | inc hostname command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result = connection.send_command("show run | inc hostname", delay_factor=2)
    # Parse the output one line at a time
    for l in result.split("\n"):
        # Split string on whitespace
        l = l.split(" ")
        if l[0] == "hostname":
            return(l[1])


def get_type(connection):
    # enter enable mode
    connection.enable()
    # execute the show run | inc hostname command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result = connection.send_command("show ver", delay_factor=2)
    # Parse the output one line at a time
    for l in result.split("\n"):
        if "Nexus Operating System" in l:
            return("cisco_nxos")
        elif "Cisco IOS" in l:
            return("cisco_ios")


def get_cdp(connection, hostname):
    # enter enable mode
    connection.enable()
    # execute the show run | inc hostname command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result1 = connection.send_command("show cdp nei", delay_factor=2)
    result2 = connection.send_command("show cdp nei detail", delay_factor=2)
    finalResult = [result1, result2]
    filename = config.outputPath + hostname + "-CDP-INFO.txt"
    # Output to file
    with open(filename,'w') as file:
        file.write(finalResult[0])
        file.write('\n\n')
        file.write(finalResult[1])


def cdp_to_csv(connection, hostname, device_type):
    parseName="false"
    firstLine="true"

    # enter enable mode
    connection.enable()
    # prepend the command prompt to the result (used to identify the local host)
    result = connection.find_prompt() + "\n"
    # execute the show cdp neighbor detail command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result += connection.send_command("show cdp neighbor det", delay_factor=2)
    # Step through output line by line
    # open the file in the write mode
    filename = config.outputPath + hostname + ".csv"
    with open(filename, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        row = ["Local Device", "Local Interface", "Remote Device", "Remote Interface"]
        # write a row to the csv file
        writer.writerow(row)
        # Parse the output one line at a time
        for l in result.split("\n"):
            # Split string on whitespace
            l = l.split(" ")
            # First line contains this devices name
            if firstLine == "true":
                firstLine = "false"
                # Strip # from end of output
                thisDevice = l[0].replace('#', '')
            # Match this is find start of new device
            if "--------------------" in l[0]:
                parseName = "true"
            elif parseName == "true":
                # This is the remote devices name
                # Split on an . to remove domain from name
                # Different for IOS and NXOS annoyingly
                if device_type == "cisco_ios":
                    deviceName = l[2].split(".")
                elif device_type == "cisco_nxos":
                    deviceName = l[1].split(".")
                # Also split on an ( to remove serial number from Nexus
                deviceName = deviceName[0].split("(")
                if device_type == "cisco_nxos":
                    #Remove ID: at beginning of nxos remote device cdp output
                    deviceName = deviceName[0].split(":")
                    deviceName = deviceName[1]
                else:
                    deviceName = deviceName[0]
                parseName = "false"
            # Match this is find start of new device
            if l[0] == "Interface:":
                # Strip any commas from interface names
                localInt = l[1].replace(',', '')
                if device_type == "cisco_ios":
                    remoteInt = l[7].replace(',', '')
                elif device_type == "cisco_nxos":
                    remoteInt = l[6].replace(',', '')
                print(thisDevice, ",", localInt, ",", deviceName, ",", remoteInt)
                row = [thisDevice, localInt, deviceName, remoteInt]
                # write a row to the csv file
                writer.writerow(row)


def get_adhoc(connection, hostname, command):
    # enter enable mode
    connection.enable()
    # execute the show run | inc hostname command
    # we increase the delay_factor for this command, because it take some time if many devices are seen by CDP
    result = connection.send_command(command, delay_factor=2)
    filename = config.outputPath + hostname + "-" + command + ".txt"
    # Output to file
    with open(filename,'w') as file:
        file.write(result)
        file.write('\n')

