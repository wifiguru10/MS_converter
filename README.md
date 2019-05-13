# MS_converter
This script will take HP switch configs and map them to meraki switches. You just need to name the meraki switch the same as the HP switch and tag it with "provision" before running the script. The script will parse through the config and configure the meraki ports, this can be done with the meraki switch online or offline. Once configured, the ports will be tagged with "API" which will make the script skip those ports in the future (for partial runs or multiple passes)


# Steps
1. place config files in input/ folder, these are raw dumps of the switch configs
2. configure the HP_convert.py script with the correct API key, ORG id and target network
3. on meraki dashboard, tag the switch with "provision" tag and name it the same as the config file (SwitchA.cfg name the MS SwitchA)
4. Run the HP_convert.py script, it'll iterate through the configs and configure the switch ports


# Requirements
1. python 3.x
2. meraki SDK for python (https://developer.cisco.com/meraki/api/#/python/getting-started)

