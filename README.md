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

# Known caveats:
-	Original config and destination port count must match (24 to 24 and 48 to 48)
-	Configs should be complete, I haven’t worked on partial configs yet
    -If you need to do partial, configure it like your doing the WHOLE switch but tag all the ports you DON’T want to change with the “api” tag
    -Ex: you want to provision a switch, but already configured the first 10 ports. Tag the first 10 with “api” tag and the script will bypass them.
-	No port-security is in the script yet, if we want to add BPDU-guard, loop-guard etc I can add it to the code
-	Script doesn’t do L3 interfaces yet, so those have to be setup manually
-	Doesn’t do LAG or auto-stacking of ports/chassis
