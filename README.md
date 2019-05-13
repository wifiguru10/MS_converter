# MS_converter


1. place config files in input/ folder, these are raw dumps of the switch configs
2. configure the HP_convert.py script with the correct API key, ORG id and target network
3. on meraki dashboard, tag the switch with "provision" tag and name it the same as the config file (SwitchA.cfg name the MS SwitchA)
4. Run the HP_convert.py script, it'll iterate through the configs and configure the switch ports

