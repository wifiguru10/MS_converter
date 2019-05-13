#!/usr/bin/python3

from datetime import datetime
from convert_library import MS_inv, MS, port
import time
import re
import os
import sys
import getopt
from meraki.meraki import Meraki

***********************************************
*****ONLY MODIFY HERE**************************
orgid = "" #organization ID
x_cisco_meraki_api_key = "" #needs R/W access
SITE = "" #name of the network, not network_id

***********************************************
***********************************************

input_path = 'input/' #directory that holds the switch configs

serialnum = "" #unused for test

SITEID = "" #unused for test

api_client = Meraki(x_cisco_meraki_api_key)

collect = {}
collect['organization_id'] = orgid
networks = api_client.networks.get_organization_networks(collect)
#print(networks)

inventory = api_client.organizations.get_organization_inventory(orgid)
#print(inventory)
tmp_switches = []


files = []

ALL_switches = []

    

def walkDir():
    for r, d, f in os.walk(input_path):
        for file in f:
            if '.cfg' in file:
                files.append(os.path.join(r,file))
    for f in files:
        print(f)

def count_interfaces(lines):
    iface_count = 0
    for l in lines:
        if "GigabitEthernet" in l:
            iface_count+=1
    return iface_count

def parse_iface(ms,lines):
    current_port = 0
    for l in lines:
        l= l.strip()
        if "interface" in l and "GigabitEthernet" in l: #this assumes interfaces are listed sequentially
            current_port +=1
            p=port()
            p.number=current_port
            ms.ports.append(p)
        if "description" in l and not "mac-address" in l: #find description and remove errors
            des=l[l.find(' '):]
    #        print(des)
            for p in ms.ports:
                if p.number == current_port:
                    if p.description=="": p.description=des.strip()
        if "link-type" in l:
            if "trunk" in l: 
                P=ms.getPort(current_port)
                if not P == "":
                    P.link_trunk = True
                    #print(l)
        if "access vlan" in l:
            P=ms.getPort(current_port)
            if not P == "":
                P.link_access = True
                b=l.split()
                if b[len(b)-1].isnumeric():
                    P.access_vlan=b[len(b)-1]
                else:
                    print("Something went wrong, cannot parse access config. not receiving numerical value")
        if "shutdown" in l:
            P=ms.getPort(current_port)
            if not P == "":
                P.enabled = False
        if "trunk permit vlan" in l and not "undo" in l:
            P=ms.getPort(current_port)
            if not P == "":
                for v in l.split():
                    if v.isnumeric(): 
                        P.trunk_allowed+=str(v)+","
                P.trunk_allowed = P.trunk_allowed[:len(P.trunk_allowed)-1]
        if "port trunk pvid vlan" in l:
            P=ms.getPort(current_port)
            if not P == "":
                t_native=l.split()
                if t_native[len(t_native)-1].isnumeric(): 
                    P.trunk_native = int(t_native[len(t_native)-1])
        if "speed " in l:
            P=ms.getPort(current_port)
            if not P == "":
                s_tmp = l.split()
                if s_tmp[len(s_tmp)-1].isnumeric():
                    P.speed = s_tmp[len(s_tmp)-1]
        if "duplex " in l:
            P=ms.getPort(current_port)
            if not P == "":
                d_tmp = l.split()
                P.duplex = d_tmp[len(d_tmp)-1]

#    for p in ms.ports:
#        print(str(p.number) + " " +p.description);

def stripit(s):
    l = re.sub('[^A-Za-z0-9]+ ', '', s)
    l = l.replace('&','')
    l = l.replace('/',' ')
    l = l.replace('-',' ')
    return l


def inv_getSwitch_name(name,raw_inv):
    for i in raw_inv:
        if name in i:
            return i
    return

def showPorts():
    for s in ALL_switches:
        print("Switch["+s.name+"] Ports["+str(len(s.ports))+"] Trunks["+str(s.trunkCount())+"] Access["+str(s.accessCount())+"]")
        for p in s.ports:
            print(p.print());

def api_load():
    for i in inventory:
        name=i['name']
        if SITE in str(name): 
            newSW = MS_inv(i)
            collect = {}
            collect['network_id']=str(i['networkId'])
            collect['serial']=str(i['serial'])
            #print(collect)
            device = api_client.devices.get_network_device(collect)
            newSW.update(device)
            print(device)
            tmp_switches.append(newSW)
            SITEID = i['networkId']

    for p in tmp_switches:
        print(str(p.print()))

    #print(site_detail)

def provision_switch(hpc, new):
    if hpc.port_count == 0: return False
    if not "provision" in new.tags: 
        print("This switch cannot be provisioned")
        print()
        return False
    c = 1
    for p in hpc.ports:
#        if c > 48: continue
        output = str(c) +" of " + str(hpc.port_count)
        c += 1 # increment
        print(output)

        collect = {}
        collect['serial'] = new.serial
        collect['number'] = p.number
        port = api_client.switch_ports.update_device_switch_port(collect)
        print(port)
        if "api" in str(port['tags']): 
            print("port already configured")
            continue 
        #print(port)
        port['name']=stripit(p.description)
        
        if p.link_trunk: 
            port['type'] = "trunk"
            port['allowedVlans'] = p.trunk_allowed
            port['vlan'] = p.trunk_native
        else: 
            port['type'] = "access"
            port['vlan'] = p.access_vlan

        port['linkNegotiation'] = 'Auto negotiate'
        if p.speed == "10" and p.duplex == "full":
            port['linkNegotiation'] =   '10 Megabit full duplex (forced)'
        if p.speed == "10" and p.duplex == "half":
            port['linkNegotiation'] =   '10 Megabit half duplex (forced)'
        if p.speed == "100" and p.duplex == "full":
            port['linkNegotiation'] =   '100 Megabit full duplex (forced)'
        if p.speed == "100" and p.duplex == "half":
            port['linkNegotiation'] =   '100 Megabit half duplex (forced)'
        if p.speed == "1000" and p.duplex == "full":
            port['linkNegotiation'] =   '1 Gigabit full duplex (forced)'
        if p.speed == "1000" and p.duplex == "half":
            port['linkNegotiation'] =   '1 Gigabit half duplex (forced)'


        port['enabled'] = p.enabled
        port['tags'] = "api"

        collect['update_device_switch_port'] = port
        print("Writing Port")
        print(collect)
        newport = api_client.switch_ports.update_device_switch_port(collect)
        print(newport)
        time.sleep(0.5)
        
    return True

def main(argv):
    print("Main loop!")
    walkDir()

    api_load()
#    site_detail = api_client.networks.get_network(SITEID)

    print()

    #read all the configs in the input directory, parse configs
    for f in files:
        F = open(f)
        lines = F.readlines()
        F.close()
        switch = MS(f.split('.')[0].split('/')[1]) #strips off the leading directory
        switch.port_count= count_interfaces(lines)
        parse_iface(switch, lines)
        ALL_switches.append(switch)

    #showPorts()

    print()

    # iterate through HP-config switches, if you find a matching meraki switch, provision
    for hpc in ALL_switches:
        #print(s.name)
        for p in tmp_switches: #for all switches in network
            if p.name == hpc.name: #found matching config for switch 
                print(p.print())
                if provision_switch(hpc, p): #source -> target
                    print("SUCCESS!")
                



if __name__ == '__main__':
    print("Starting")
    main(sys.argv[1:])




