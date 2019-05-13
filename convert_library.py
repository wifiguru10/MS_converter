#!/usr/bin/python3

class MS_inv:
    claimedAt = ""
    name = ""
    serial = ""
    model = ""
    mac = ""
    publicIp = ""
    networkId = ""
    status = ""
    lanIp = ""
    netId = ""
    address = ""

    tags = ""

    def __init__(self, raw_inv):
#        print("loading object")
#        print(raw_inv)
        self.name = raw_inv['name'] 
        self.serial = raw_inv['serial']
        self.mac = raw_inv['mac']
        self.publicIp = raw_inv['publicIp']
        self.networkId = raw_inv['networkId']
        self.model = raw_inv['model']
        self.claimedAt = raw_inv['claimedAt']

    def update(self,device):
        self.lanIp = device['lanIp']
        self.address = device['address']
        self.tags = device['tags']


    def print(self):
        output = "Name["+self.name+"] SN["+self.serial+"] MAC["+self.mac+"] "
        output+= "PubIP["+str(self.publicIp)+"] netID["+self.networkId+"] "
        output+= "Model["+self.model+"] Claimed["+str(self.claimedAt)+"] "
        output+= "LanIP["+str(self.lanIp)+"] Tags["+self.tags+"] Address["+self.address+"]"
        return output


class MS:
    name = ''
    port_count = 0
    ports = []

    def __init__(self,name):
        self.name=name
        self.ports= [] #has to be initialized here, otherwise its == across all objects
        print("Loaded HP Config for Switch["+self.name+"]")

    def getPort(self, num):
        for p in self.ports:
            if p.number == num: return p
        return "" 

    def accessCount(self):
        access_count=0
        for p in self.ports:
            if p.link_access == True: access_count+=1
        return access_count

    def trunkCount(self):
        trunk_count=0
        for p in self.ports:
            if p.link_trunk == True: trunk_count+=1
        return trunk_count


class port:
    description = ''
    tags = ''
    number = 0
    enabled = True
    link_trunk = False
    link_access = False
    trunk_native = 1
    trunk_allowed = ''
    access_vlan = 1
    speed = 'auto'
    duplex = 'auto'

    def __init__(self):
        self.description = ''
        self.tags = ''
        self.number = 0

    def print(self):
        output="Port[" + str(self.number) + "] Type["
        if self.link_trunk: 
            output += "TRUNK] Native[" + str(self.trunk_native) +"]  Allowed[" + self.trunk_allowed.strip() + "]"
        else: 
            output += "ACCESS] VLAN["+str(self.access_vlan)+"] "
        output+= " DESC["+self.description+"] TAGS["+self.tags+"] Speed[" + self.speed + "] Duplex[" + self.duplex + "] Enabled[" + str(self.enabled) + "]"
        
        return output
    

