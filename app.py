#Inseego 5G SD EDGE Manager PythonTool
#Copyright 2023 Ryan Kendrick and Inseego ryan.kendrick@inseego.com
import INSGEMPT,json,pprint,time,sys,time
#,statistics,ipaddress,uuid
#mydata={'device_id': 92, 'device_name': '5GAusCBRTAM1', 'device_model': 'V2000', 'device_serial': 'FN0000000V2000', 'hostname': 'V2000-1138-af58', 'device_firmware_version': '2022.22.1.0', 'device_model_number': '', 'device_imei': 'NA', 'device_mac': '60:45:bd:26:af:58', 'tenant_id': None, 'is_approved': True, 'is_headendcpe': '1', 'platform': 1, 'device_eth_wan_ip': '20.37.1.132', 'device5g_interface_ip': '', 'device_control_tunnel_ip': '10.171.0.85', 'device_wg_pubkey': 'qd1XQGb/UjxqRP0gbyqQ/yFAP2KEGOO3jPYWWwQxhAY=', 'device_md5': '2efbc8704df69db8e7f1242933eb3ffb', 'device_username': 'U2FsdGVkX19QdlPmw+cXIHSzaLfIIRIK4XiOkeGQ3t0=', 'device_password': 'U2FsdGVkX1/76ZHzEPe497E1cwx3oH9F5s7J6Yk+Y2Y8+Pp2y9i7atkBzYJyczC4', 'device_status': 1, 'device_configured_date': '2023-03-21T01:14:18.926252Z', 'created_by': '', 'created_date': '2023-03-21T01:13:53.050118Z', 'updated_by': 'sdwan_admin', 'updated_date': '2023-03-21T01:19:19.883205Z', 'device_location': '-', 'device_delete_status': 0, 'z_host_id': 10645, 'z_template_id': 10644, 'zabbix_template_version': '', 'eth_port_status': {'eth0': 1, 'eth1': 0, 'eth2': 0, 'eth3': 0, 'eth4': 0, 'eth5': 0, 'eth6': 0, 'eth7': 0, 'radio_2g': 0, 'radio_5g': 0, 'usb.status': 0, 'rmnet_data0': 0}, 'is_fixed_ip': 0, 'device_public_data_key': '', 'is_deleted': '0', 'guacamole_identifier': 116, 'supported_templates': {'Reboot': 1, 'DataTunnel': 1, 'SysUpgrade': 1, 'KeyRotation': 1, 'StaticRoute': 1, 'DeleteDevice': 1, 'BootstrapReset': 1, 'Troubleshooting': 1, 'BGPConfiguration': 1, 'QoSConfiguration': 1, 'WANConfiguration': 1, 'OSPFConfiguration': 1, 'SystemConfiguration': 1, 'NetworkConfiguration': 1, 'FirewallConfiguration': 1, 'DNSFilteringConfiguration': 1}, 'is_pinned': True, 'pf_root_password': '', 'modem_version': '-', 'is_ippt': False, 'is_hub': False, 'group_name': ''}
title="""
 _____ 
|_   _|
  | | _ __  ___  ___  ___  __ _  ___ 
  | || '_ \/ __|/ _ \/ _ \/ _` |/ _ \ 
 _| || | | \__ \  __/  __/ (_| | (_) |
 \___/_| |_|___/\___|\___|\__, |\___/
                           __/ |                     
                          |___/
"""

if __name__ == "__main__":
	print(title)
	MyConfig=INSGEMPT.GetConfig()
	MyEM=INSGEMPT.EMHandler(MyConfig)
	MyEM.Populate()
	MyEM.ApplyIPPTfromCSV("modem_dmz.csv")
	#for obj in MyEM.Nodes:
	#	print(obj.Device.eth_port_status)
	
	
	#MyEM.ApplyIPPTfromCSV("my.csv")
	
	#pprint.pprint(MyEM.Nodes[4].OSPFConfiguration.GeneratePayload())
	#MyEM.Nodes[4].OSPFConfiguration.AddRedistribution(['bgp'])
	#MyArea={"id": "0IJ8XGPIB","area": "0",
	#	"cost": "",
	#	"keyID": "",
	#	"network": "Default",
	#	"authType": "none",
	#	"password": "",
	#	"priority": "1",
	#	"deadTimer": "40",
	#	"interface": "br-lan",
	#	"isdeleted": "0",
	#	"helloTimer": "10",
	#	"transmitDelay": "1",
	#	"advancedOptions": "1",
	#	"retransmitInterval": "5"
	#}
	#MyEM.Nodes[4].OSPFConfiguration.AddArea(MyArea)
	#pprint.pprint(MyEM.Nodes[4].OSPFConfiguration.GeneratePayload())
	#MyEM.Nodes[4].ApplyTemplate("OSPF",MyEM.Nodes[4].OSPFConfiguration.GeneratePayload())
	#MyFile=sys.argv[1]
	#if not MyFile: exit()
	#mydata=MyEM.Nodes.Serialize()
	#INSGEMPT.WritetoJSON(mydata,'mydata.json')
	#MyPayload=ReadfromFile("payload.json")
	#MyApply=MyEMHandler.applyTemplate(MyPayload)
	#derp=Tree()
	#derp.Root=Child(1)
	#derp.Root.AddChild(Child(2))
	#derp.Root.GetChildren()[0].AddChild(Child(4))
	#derp.Root.GetChildren()[0].GetChildren()[0].AddChild(Child(5))
	#derp.Root.AddChild(Child(3))
	#derp.Root.GetChildren()[1].AddChild(Child(6))
	#pprint.pprint(derp.Serialize())
	#derp.RemoveChild(derp.Root,derp.Root.Children[0])
	#pprint.pprint(derp.Serialize())
	#derp.RelocateChild(derp.Root.Children[0],derp.Root.Children[0].Children[0],derp.Root.Children[1])
	#pprint.pprint(derp.Serialize())
	#mykeys=ObjectList()
	#data=ReadfromJSON("out.json")
	#for o in data["Objects"]:
	#	mykeys.AddObjects([Device(**o)])
	#mykeys.AddLinks(data["Links"])
	#for o in mykeys.Objects:
	#	for m in mykeys.Objects:
	#		mykeys.AddLinks([(m.device_id,o.device_id)])
	#mydata=mykeys.Serialize()
	#WritetoJSON(mydata,"out.json")
	#mykeys.AddLinks([(mykeys.Objects[0],mykeys.Objects[1])])
	#derp=data[1]["results"][0].keys()

	#data=MyEMHandler.listTemplate()
	#WritetoJSON(data,"templates.json")
	#data=ReadfromJSON("data.json")
	#derp=ObjectList()
	#for obj in data:
	#	derp.AddObjects([Device(**obj)])
	#times=[]
	#for i in range(1000):
	#	starttime=time.time()
	#	blah=derp.FindObjects({"device_name":"V2000-0000-2"})
	#	delta=time.time()-starttime
	#	times.append(delta)
	#print(statistics.mean(times))
	#times=[]
	#for i in range(1000):
	#	starttime=time.time()
	#	blah=derp.FindObjects({'device_id':90})
	#	delta=time.time()-starttime
	#	#print("",delta)
	#	times.append(delta)
	#	#print(blah)
	#print(statistics.mean(times))
	#
	#MyNet=MyEMHandler.networkView(**{"device_id":70})
		
