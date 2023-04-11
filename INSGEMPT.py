#Inseego 5G SD EDGE Manager PythonTool
#Copyright 2023 Ryan Kendrick and Inseego ryan.kendrick@inseego.com
#Work in progress. Use at your own risk.

import requests,json,pprint,csv,time

def GetConfig(configfile="config.json"):
	config=json.loads(open(configfile,"r").read())
	baseurl = config["baseurl"]
	basicauth = config["basicauth"]
	return(config)
class APIRequest():
	def __init__(self,method='',url={},headers={},payload={},files=[]):
		self.method=method
		self.headers=headers
		self.payload=payload
		self.url=url
		self.files=files
	def Execute(self):
		method=self.method
		url=self.url
		headers=self.headers
		data=self.payload
		files=self.files
		#pprint.pprint(method)
		#pprint.pprint(url)
		#pprint.pprint(headers)
		#pprint.pprint(data)
		#pprint.pprint(files)
		response = requests.request(method=method, url=url, headers=headers, data=data, files=files)
		return response
class APIHandler():
	def __init__(self,baseurl,basicauth):
		self.headers={}
		self.baseurl=baseurl
		self.basicauth=basicauth
	def GenerateBearer(self):
		self.headers["Authorization"]="Bearer "+self.MakeRequest('POST',{'Authorization': 'Basic '+self.basicauth},{},"api-user/login/",[])[1]["access"]
	def MakeRequest(self,method,headers,payload,suburl,files):
		url=self.baseurl+suburl
		myrequest = APIRequest(method, url, headers, payload,files)
		myexecout=myrequest.Execute()
		#pprint.pprint(method)
		#pprint.pprint(headers)
		#pprint.pprint(payload)
		#pprint.pprint(suburl)
		#pprint.pprint(files)
		#pprint.pprint(myexecout)
		#pprint.pprint(myexecout.text)
		myout=''
		if myexecout.text: myout=json.loads(myexecout.text)
		return [myexecout.status_code,myout]
	def MakeRequestWithBearer(self,method,headers,payload,suburl,files={}):
		if not "Authorization" in self.headers:
			self.GenerateBearer()
			#print(self.headers)
		headers["Authorization"]=self.headers["Authorization"]
		count=0
		while True:
			#headers=self.headers
			output=self.MakeRequest(method,headers,payload,suburl, files)
			#print(str(output))
			if output[0]==401 and count<5:
				self.GenerateBearer()
				count+=1
				print(count)
				if count>3: return("Error getting Bearer")
			else:
				break
		return(output)
class EMAPIHandler(APIHandler):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
	def tunnelStatusFilter(self,tunnel_data,next=''):
		#9.4.	Tunnel Status
		url="device/tunnelStatusFilter"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"tunnel_data": tunnel_data})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def tunnelSearch(self,tunnel_data,next=''):
		#9.3.	Search Tunnel
		url="device/tunnelSearch"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"tunnel_data": tunnel_data})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def searchDefaultTemplateList(self,template_data,next=''):
		#6.17.	Searching Default Template List
		url="device/searchDefaultTemplateList"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_data": template_data})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def searchTemplateList(self,template_data,next=''):
		#6.16.	Search Template List
		url="device/searchTemplateList"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_data": template_data})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def searchDeviceList(self,device_data,next=''):
		#2.10.	Search Device List
		url="device/searchDeviceList"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_data": device_data})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def groupDevicesInfo(self,group_id,next=''):
		#2.30.	Group Devices Information
		url="device/groupDevicesInfo"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def deviceGroupAppliedTemplates(self,group_id):
		#6.3.	Device Group Applied Template Information
		url="device/deviceGroupAppliedTemplates"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def getDeviceEventFilter(self,device_name,severity):
		#2.25.	Device Events Filter
		url="device/getDeviceEventFilter"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_name": device_name,"severity":severity})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def getNewModelList(self,device_model='',next=''):
		#2.37/38.	Unconfigured Devices Filter
		url="device/getNewModelList"+next
		if device_model:
			headers={}
			headers["Content-Type"]="application/json"
			payload = json.dumps({"device_model": device_model})
			output=self.MakeRequestWithBearer("POST",headers,payload,url)
		else:
			output=self.MakeRequestWithBearer("POST",{},{},url)
		return(output)
	def newDeviceListInfo(self,device_model):
		#2.36.	Unconfigured Device List
		url="device/newDeviceListInfo"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_model": device_model})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
	def groupInfoByModel(self,device_model):
		#2.39.	Group Information
		url="device/groupInfoByModel"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_model": device_model})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
	def groupsByModel(self,device_model):
		#2.10.	Search Device List
		url="device/groupsByModel"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_model": device_model})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def listTemplate(self,next=''):
		#6.10.	Template List
		url="device/listTemplate"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def initiateTunnel(self,device_mac=''):
		#9.5/6.	Initiating Tunnel GET shows available devices for tunnel creation;post method will be give the tunnel data by device_mac
		url="device/initiateTunnel"
		if device_mac:output=self.MakeRequestWithBearer("POST",{},{},url)
		else: output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def createTunnel(self):
		pass
		#9.7.	Creating New Tunnel between two devices
	def tunnelListFilter(self,next=''):
		#9.2.	Tunnel List Filtering Data
		url="device/tunnelListFilter"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def tunnelList(self,next=''):
		#9.2.	Tunnel List Filtering Data
		url="device/tunnelList"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def moduleList(self):
		#8.1.	Module List
		url="device/moduleList"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def GetUsers(self,next=''):
		#3.1.	List of Users
		url="api-user/users/"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def configuredDeviceList(self,next=''):
		#2.14.	Configured Devices
		url="device/configuredDeviceList"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def downloadOperationLogfile(self):
		#2.14.	Configured Devices
		url="device/downloadOperationLogfile"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def unconfiguredDeviceList(self,next=''):
		#2.13.	Unconfigured Devices
		url="device/unconfiguredDeviceList"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def deviceGroupModelCount(self):
		#5.1.	Model Count Group Dashboard View
		url="device/deviceGroupModelCount"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def modelcount(self):
		#5.6.	Model Count Home Dashboard View
		url="device/modelcount"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def totaldevices(self):
		#5.2.	Total Device Home Dashboard View
		url="device/totaldevices"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def cpedevices(self):
		#5.3.	CPE Device Home Dashboard View
		url="device/cpedevices"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def mifidevices(self):
		#5.4.	Mifi Home Dashboard View
		url="device/mifidevices"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def tunnelcount(self):
		#5.5.	Tunnel Home Dashboard View
		url="device/tunnelcount"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def getDeviceOperations(self,next=''):
		#4.3.	Device Operation Validation
		#4.4.	Device Operation Information
		url="device/getDeviceOperations"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def downloadDeviceLogfile(self):
		#2.48.	Downloading Device Snapshot
		url="device/downloadDeviceLogfile"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def networkTopology(self):
		#2.49.	Network Topology
		url="device/networkTopology"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def DeviceLookUp(self,device_model='',device_id=''):
		#2.15.	Device Lookup
		headers={}
		headers["Content-Type"]="application/json"
		MyPayload={}
		if device_model:MyPayload["device_model"]=device_model
		if device_id:MyPayload["device_id"]=device_id
		payload = json.dumps(MyPayload)
		url="device/DeviceLookUp"
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
		url="device/DeviceLookUp"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def testZabbixTemplates(self,host_id,template_id):
		#6.11.	Testing Zabbix Templates
		#payload or url stuff with host_id,template_id???
		url="device/testZabbixTemplates"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def deviceGroupLookUp(self):
		#2.16.	Device Group Lookup
		url="device/deviceGroupLookUp"
		output=self.MakeRequestWithBearer("GET",{},{},url)
	def templatesDropdown(self):
		#6.12.	Template Drop Down
		#Listing template_name and template_id in dropdown
		url="device/templatesDropdown"
		output=self.MakeRequestWithBearer("GET",{},{},url)
	def bootstrapTempDropdown(self):
		#6.13.	Bootstrap Template Drop Down
		#Listing template_name and template_id in dropdown
		url="device/bootstrapTempDropdown"
		output=self.MakeRequestWithBearer("GET",{},{},url)
	def firmwareDownload(self):
		#2.55.	Firmware Download 
		url="device/firmwareDownload"
		output=self.MakeRequestWithBearer("GET",{},{},url)
	def deviceLookUpGroup(self):
		#2.31.	Device Lookup \n Name: Device Lookup Group
		url="device/deviceLookUpGroup"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def deviceGroupList(self,next=''):
		#2.6.	Device Group Information
		#2.60.	Device Group Information
		url="device/deviceGroupList"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def defaultTemplateList(self,next=''):
		#6.5.	Default Template List
		url="device/defaultTemplateList"+next
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def templateinfo(self):
		#returning no data, need to look into more
		url="device/templateinfo"
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def groupNetworks(self):
		#2.11.	Device Group Network View
		url="device/groupNetworks"
		output=self.MakeRequestWithBearer("POST",{},{},url)
		return(output)
	def groupTemplateInfo(self,group_id):
		#6.1.	Group Templates Information
		url="device/groupTemplateInfo"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def CreateUser(self,group_id):
		#3.2.	Create New User
		url="api-user/register/"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({})#give me some payload
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def groupDevicesDataUsageByModel(self,group_id,start_date,end_date):
		#2.26.	Group Device Data 
		url="device/groupDevicesDataUsageByModel"
		payload = json.dumps({"group_id": group_id,"start_date":start_date,"end_date":end_date})
		output=self.MakeRequestWithBearer("POST",{},payload,url)
		return(output)
	def dataUsageReset(self):
		#2.27.	Data Usage Reset
		url="device/dataUsageReset"
		output=self.MakeRequestWithBearer("POST",{},{},url)
		return(output)
	def deviceGroupDataUsage(self,group_id,start_date,end_date,day_no):
		#2.28.	Grouped Devices Data Usage
		url="device/deviceGroupDataUsage"
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"group_id": group_id,"start_date":start_date,"end_date":end_date,"day_no":day_no})
		output=self.MakeRequestWithBearer("POST",{},{},url)
		return(output)
	def groupDeviceEvent(self,group_id):
		#2.24.	Device Group Events
		url="device/groupDeviceEvent"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",{},payload,url)
		return(output)
	def deviceGroupReboot(self,group_id):
		#2.21.	Group Reboot
		url="device/deviceGroupReboot"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",{},payload,url)
		return(output)
	def deviceGroupFactoryReset(self,group_id):
		#2.22.	Group Factory Reset
		url="device/deviceGroupFactoryReset"
		payload = json.dumps({"group_id": group_id})
		output=self.MakeRequestWithBearer("POST",{},payload,url)
		return(output)
	def uploadTemplate(self,template_payload):
		#6.19.	Uploading Template Information
		#files=[('file',('blah.json',template_payload,'application/json'))]
		#files=[('file',('blah1.json',open('blah1.json','rb'),'application/json'))]
		files=[('file',('blah1.json',template_payload,'application/json'))]
		#pprint.pprint(files)
		#pprint.pprint(open('blah1.json','rb'))
		output=self.MakeRequestWithBearer("POST",{},{},"device/uploadTemplate",files)
		return(output)
	def WgKeyExchange(self,payload):
		#9.1.	CreateWG Tunnel
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/WgKeyExchange")
		return(output)
	def applyTemplate(self,payload):
		#6.6.	Apply Template
		headers={}
		headers["Content-Type"]="application/json"
		#pprint.pprint(payload)
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/applyTemplate")
		pprint.pprint(output)
		return(output)
	def editTemplate(self,template_id,payload):
		#6.7.	Editing Template Info
		#6.8.	Edit Template method GET
		headers={}
		headers["Content-Type"]="application/json"
		url="device/applyTemplate"+"/"+template_id
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		return(output)
	def setAsDefaultZTPTemplates(self,payload):
		#6.4.	Default Template
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/setAsDefaultZTPTemplates")
		return(output)
	def setAsFactoryTemplate(self,payload):
		#6.14.	Set As Factory Templates
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/setAsFactoryTemplate")
		return(output)
	def createTemplate(self,payload):
		#6.2.	Creating Template Information
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/createTemplate")
		return(output)
	def deleteTemplate(self,template_name):
		#6.9.	Deleting Template Information
		headers={}
		headers["Content-Type"]="application/json"
		payload=json.dumps({"template_name":template_name})#need payload
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deleteTemplate")
		return(output)
	def deleteDeviceGroup(self):
		#2.7.	Deleting Device Group
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,{},"device/deleteDeviceGroup")
		return(output)
	def addDeviceGroup(self):
		#2.9.	Adding Device Group
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,{},"device/addDeviceGroup")
	def deviceLogDownload(self,device_id=""):
		#2.45.	Downloading Device Log
		#2.58.	Generating MA log file GET method
		#2.59.	Download Log File specify device_id
		headers={}
		headers["Content-Type"]="application/json"
		output=self.MakeRequestWithBearer("POST",headers,{},"device/deviceLogDownload")
	def editTunnel(self,tunnel_id,payload):
		#9.8.	Editing Tunnel Information
		headers={}
		headers["Content-Type"]="application/json"
		url="device/editTunnel"+"/"+tunnel_id
		output=self.MakeRequestWithBearer("PUT",headers,payload,url)
		return(output)
	def updateDeviceGroup(self,group_id):
		#2.8.	Updating Device Group
		headers={}
		headers["Content-Type"]="application/json"
		url="device/updateDeviceGroup"+"/"+group_id
		output=self.MakeRequestWithBearer("PUT",headers,{},url)
		return(output)
	def UpdateUser(self,user_id,first_name,last_name,email_address,user_role,user_enabled):
		#3.5.	Updating User Information
		headers={}
		headers["Content-Type"]="application/json"
		url="api-user/"+user_id
		payload={}#give me a payload
		output=self.MakeRequestWithBearer("PUT",headers,payload,url)
		return(output)
	def ChangePassword(self,user_id,password):
		#3.7.	Changing Password
		headers={}
		headers["Content-Type"]="application/json"
		url="api-user/change-password/"
		payload={}#give me a payload
		output=self.MakeRequestWithBearer("PUT",headers,payload,url)
		return(output)
	def getDeviceDetails(self,device_id):
		#2.35.	Device Details
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/getDeviceDetails")
		return(output)
	def tunnelInfo(self,device_mac='',tunnel_id=''):
		#9.9.	Tunnel Information
		headers={}
		headers["Content-Type"]="application/json"
		MyPayload={}
		if device_mac: MyPayload["device_mac"]=device_mac
		if tunnel_id: MyPayload["tunnel_id"]=tunnel_id
		payload = json.dumps(MyPayload)
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/tunnelInfo")
		return(output)
	def updateDeviceName(self,device_id,device_name):
		#2.61.	Update Device Name
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id,"device_name":device_name})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/updateDeviceName")
		return(output)
	def networkView(self,device_id):
		#2.50.	Network View
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/networkView")
		return(output)
	def clientList(self,device_id):
		#2.29.	Connecting Clients Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/clientList")
		return(output)
	def attachedDeviceInfo(self,template_id):
		#2.5.	Attached Device Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"template_id": template_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/attachedDeviceInfo")
		return(output)
	def taskCancellation(self,task_id):
		#7.1.	Celery Task
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"task_id": task_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/taskCancellation")
		return(output)
	def getTemplateByTemplateId(self,template_id):
		#6.20.	Template Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"template_id": template_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/getTemplateByTemplateId")
		return(output)
	def addDevice(self,device_mac,approve_status=1,is_fixed_ip=0):
		#2.23.	Adding Device
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac,"approve_status":approve_status,"is_fixed_ip":is_fixed_ip})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/addDevice")
		return(output)
	def updateFixedIp(self,device_id,is_fixed_ip=0):
		#2.56.	Update Fixed IP
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id":device_id,"is_fixed_ip":is_fixed_ip})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/updateFixedIp")
		return(output)
	def init(self,device_mac,device_ctunnel_ip,device_lan_ip,device_guest_ip,device_lan_cidr,device_password):
		#2.18.	Initiating Device
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac,"device_ctunnel_ip":device_ctunnel_ip,"device_lan_ip":device_lan_ip,"device_guest_ip":device_guest_ip,"device_lan_cidr":device_lan_cidr,"device_password":device_password})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/init")
		return(output)
	def applyDefaultZTPconfig(self,device_mac):
		#6.15.	Default ZTP Configs Apply
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/applyDefaultZTPconfig")
		return(output)
	def deleteDevicedup(self,device_mac):
		#2.17.	Deleting Device Data
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deleteDevice")
		return(output)
	def tunnelView(self,device_mac):
		#9.11.	Tunnel View Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/tunnelView")
		return(output)
	def groupTunnelView(self,group_id):
		#9.12.	Group Tunnel View Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"group_id":group_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/groupTunnelView")
		return(output)
	def checkDeviceTask(self,device_mac):
		#2.44.	Checking Device Task
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/checkDeviceTask")
		return(output)
		#It will get True if Device have pending  operations and False for if device have In Progress Task
	def deviceCheckpoints(self,device_mac,is_delete=False):
		#2.40.	Creating Device Backup
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac,"is_delete":is_delete})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deviceCheckpoints")
		return(output)
	def restoreDeviceCheckpoints(self,checkpoint_id):
		#2.41.	Restoring Device Backup
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"checkpoint_id":checkpoint_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/restoreDeviceCheckpoints")
		return(output)
	def ListdeviceCheckpoints(self,device_mac):
		#2.42.	Listing Device Checkpoints
		#https://dev.inseego5g.net:7001/device/deviceCheckpoints?device_mac=28:80:a2:c6:39:41
		url="device/deviceCheckpoints"+"?device_mac="+device_mac
		output=self.MakeRequestWithBearer("GET",{},{},url)
		return(output)
	def DeletedeviceCheckpoint(self,device_mac):
		#2.43.	Deleting Device Backup
		url="device/deviceCheckpoints"+"?device_mac="+device_mac
		output=self.MakeRequestWithBearer("DELETE",{},{},url)
		return(output)
	def Logout(self):
		#3.4.	Logout
		url="api-user/logout/"
		output=self.MakeRequestWithBearer("POST",{},{},url)
		return(output)
	def DeleteUser(self,user_id):
		#3.3.	Delete User Information
		url="api-user/"+user_id
		output=self.MakeRequestWithBearer("DELETE",{},{},url)
		return(output)
	def deviceTroubleshooting(self):
		#2.57.	Device Troubleshooting
		output=self.MakeRequestWithBearer("POST",{},{},"device/deviceTroubleshooting")
		return(output)
	def updateOperationStatus(self,operation_id):
		#4.1.	Update Operation Status 
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"operation_id": operation_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/updateOperationStatus")
		#It will make the inQueue Operation as failed manually
		return(output)
	def appliedTemplatelist(self,device_id,next=''):
		url="device/appliedTemplatelist"+next
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,url)
		#It will make the inQueue Operation as failed manually
		return(output)
	def operationLog(self,operation_id):
		#4.5.	Operation Log Details
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"operation_id": operation_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/operationLog")
		#It will make the inQueue Operation as failed manually
		return(output)
	def deleteDevice(self):
		#2.33.	Connecting Device
		output=self.MakeRequestWithBearer("POST",{},{},"device/connectDevice")
		return(output)
	def firmwareUpgrade(self):
		#2.51.	Firmware Upgrade
		output=self.MakeRequestWithBearer("POST",{},{},"device/firmwareUpgrade")
		return(output)
	def createHost(self,device_ip):
		#3.6.	Create Host
		headers={}
		headers["Content-Type"]="application/json"
		payload={}#need payload
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/createHost")
		return(output)
	def firmwarelistfilter(self):
		#2.52.	Firmware Filter
		output=self.MakeRequestWithBearer("POST",{},{},"device/firmwarelistfilter")
		return(output)
	def firmwareUpgradeStatus(self):
		#2.53.	Firmware Upgrade Status
		output=self.MakeRequestWithBearer("POST",{},{},"device/firmwareUpgradeStatus")
		return(output)
	def firmwareVersions(self):
		#2.54.	Firmware Versions
		output=self.MakeRequestWithBearer("POST",{},{},"device/firmwareVersions")
		return(output)
	def downloadConfigFile(self):
		#2.47.	Download Config File
		output=self.MakeRequestWithBearer("POST",{},{},"device/downloadConfigFile")
		return(output)
	def deviceWireguardInfo(self,device_mac,device_public_key):
		#2.32.	Device Wire Guard Information
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_mac":device_mac,"device_public_key":device_public_key})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deviceWireguardInfo")
		return(output)
	def approveDevice(self,approved_device):
		#2.34.	Approve Device
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"approved_device":[approved_device]})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/approveDevice")
		return(output)
	def modemInfo(self,device_id):
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/modemInfo")
		return(output)
	def downloadTemplate(self,template_id):
		#6.18.	Downloading Templates 
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"template_id": template_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/downloadTemplate")
		return(output)
	def deviceStatistics(self,device_id):
		#2.19.	Device Statics
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deviceStatistics")
		return(output)
	def deviceConnectivityReset(self,device_id):
		#2.20.	Reset Device Connectivity
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/deviceConnectivityReset")
		return(output)
	def networkViewdup(self,device_id):
		headers={}
		headers["Content-Type"]="application/json"
		payload = json.dumps({"device_id": device_id})
		output=self.MakeRequestWithBearer("POST",headers,payload,"device/networkView")
		return(output)
	def deviceEvents(self,device_id='',next=''):
		url="device/deviceEvents"+next
		headers={}
		headers["Content-Type"]="application/json"
		if device_id:
			payload = json.dumps({"device_id": device_id})
			output=self.MakeRequestWithBearer("POST",headers,payload,url)
			#2.2.	Particular Device Events Information
		else:
			output=self.MakeRequestWithBearer("GET",headers,{},url)
			#2.1.	All Device Events Information
		return(output)
	def deviceSeverity(self,device_id=''):
		headers={}
		headers["Content-Type"]="application/json"
		url="device/deviceSeverity"
		if device_id:
			payload = json.dumps({"device_id": device_id})
			output=self.MakeRequestWithBearer("POST",headers,payload,url)
			#2.4.	Specific device severity count
		else:
			output=self.MakeRequestWithBearer("GET",headers,{},url)
			#2.3.	Device Severity Count
		return(output)
	def GetAllTunnels(self):
		results=[]
		mylist=self.tunnelList()
		#pprint.pprint(derp)
		for obj in mylist[1]["results"]:
			results.append(obj)
		while True:
			if mylist[1]["next"]:
				next=mylist[1]["next"]
				#next=next.replace("http:","https:").replace(":7000",":7001")
				next=next[next.index('?'):]
				#pprint.pprint(next)
				mylist=self.tunnelList(next)
				for obj in mylist[1]["results"]:
					results.append(obj)
			else: break
		return(results)
	def GetAllNetworks(self,device_ids=[]):
		results=[]
		for d in device_ids:
			mylist=self.networkView(**{"device_id":d})
			results.append({'device_id':d,'networks':mylist[1]["data"]})
		return(results)
	def GetAllTemplates(self):
		results=[]
		mylist=self.listTemplate()
		#pprint.pprint(derp)
		for obj in mylist[1]["results"]:
			results.append(obj)
		while True:
			if mylist[1]["next"]:
				next=mylist[1]["next"]
				#next=next.replace("http:","https:").replace(":7000",":7001")
				next=next[next.index('?'):]
				#pprint.pprint(next)
				mylist=self.listTemplate(next)
				for obj in mylist[1]["results"]:
					results.append(obj)
			else: break
		return(results)
	def GetAllappliedTemplatelist(self,device_id):
		results=[]
		mylist=[self.appliedTemplatelist(device_id)]
		#pprint.pprint(derp)
		for obj in mylist[1]["results"]:
			results.append(obj)
		while True:
			if mylist[1]["next"]:
				next=mylist[1]["next"]
				#next=next.replace("http:","https:").replace(":7000",":7001")
				next=next[next.index('?'):]
				#pprint.pprint(next)
				mylist=self.appliedTemplatelist(device_id,next)
				for obj in mylist[1]["results"]:
					results.append(obj)
			else: break
		return(results)
	def GetAllDevices(self):
		results=[]
		mylist=self.configuredDeviceList()
		#pprint.pprint(derp)
		for obj in mylist[1]["results"]:
			results.append(obj)
		while True:
			if mylist[1]["next"]:
				next=mylist[1]["next"]
				#next=next.replace("http:","https:").replace(":7000",":7001")
				next=next[next.index('?'):]
				#pprint.pprint(next)
				mylist=self.configuredDeviceList(next)
				for obj in mylist[1]["results"]:
					results.append(obj)
			else: break
		return(results)
	def GetAllDevicesDetails(self):
		results=[]
		mydevices=self.GetAllDevices()
		for obj in mydevices:
			mydev=self.getDeviceDetails(obj["device_id"])
			#pprint.pprint(obj["device_id"])
			results.append(mydev[1]["data"][0])
		return(results)
	def GetAllDevicesClients(self,device_ids=[]):
		results=[]
		if not device_ids:
			mydevices=self.GetAllDevices()
			for o in mydevices:
				device_ids.append(o["device_id"])
		for D in device_ids:
			mydev={}
			mydev["device_id"]=D
			mydev["clients"]=self.clientList(D)[1]["data"]
			#pprint.pprint(obj["device_id"])
			results.append(mydev)
		return(results)
class ObjectList(list):
	def __init__(self):
		#self.Objects=[]
		#self.Links=[]
		pass
	def AddObjects(self,Objects):
		for obj in Objects:
			if obj not in self: self.append(obj)
	def RemoveObjects(self,Objects):
		for obj in Objects:
			if obj in self: self.remove(obj)
	def FindObjects(self,criteria):
		foundobjects=[]
		for object in self:
			found=True
			for criterion in criteria.keys():
				found=getattr(object,criterion)==criteria[criterion]*found
			if found:
				foundobjects.append(object)
		return(foundobjects)
	#def AddLinks(self,links):
	#	for l in links:
	#		self.Links.append(l)
	#def GetLinks(self,object):
	#	links=[]
	#	for l in self.Links:
	#		if object in l: links.append(l)
	#	return(links)
	def Serialize(self):
		data={}
		objects=[]
		for o in self:
			if type(o) is dict:
				objects.append(o)
			else:
				objects.append(o.Serialize())
		data=objects
		#links=[]
		#for l in self.Links:
		#	links.append(l)
		#data["Links"]=links
		return(data)
class EMHandler():
	def __init__(self,MyConfig):
		self.EMAPIHandler=EMAPIHandler(**MyConfig)
		self.Devices=ObjectList()
		self.Tunnels=ObjectList()
		self.Templates=ObjectList()
		#self.Networks=ObjectList()
		self.Nodes=ObjectList()
		#super().__init__()
	def Serialize(self):
		mydump={}
		#mydump["Devices"]=self.Devices.Serialize()
		#mydump["Networks"]=self.Networks.Serialize()
		#mydump["Tunnels"]=self.Tunnels.Serialize()
		mydump["Templates"]=self.Templates.Serialize()
		mydump["Nodes"]=self.Nodes.Serialize()
		return(mydump)
	def DeviceLookUp(self,**kwargs):
		MyData=self.EMAPIHandler.DeviceLookUp(**kwargs)
		return(MyData)
	def ApplyTemplate(self,payload):
		mydata=self.EMAPIHandler.applyTemplate(payload)
		return(mydata)
	def PopulateDevices(self,MyData=''):
		print("PopulateDevices")
		if MyData:
			pass
		else: MyData=self.EMAPIHandler.GetAllDevicesDetails()
		for obj in MyData:
			MyDevice=Device(**obj)
			self.Devices.AddObjects([MyDevice])
			MyNode=Node(Parent=self,MyDevice=MyDevice)
			self.Nodes.AddObjects([MyNode])
		return MyData
	def PopulateTunnels(self,MyData=False):
		print("PopulateTunnels")
		if MyData:
			pass
		else: MyData=self.EMAPIHandler.GetAllTunnels()
		#pprint.pprint(MyData)
		for obj in MyData:
			MyTun=Tunnel(**obj)
			MyDevA=self.Nodes.FindObjects({'device_mac':obj["device_A_mac"]})[0]
			MyDevB=self.Nodes.FindObjects({'device_mac':obj["device_B_mac"]})[0]
			self.Tunnels.AddObjects([MyTun])
			MyDevA.Tunnels.AddObjects([MyTun])
			MyDevB.Tunnels.AddObjects([MyTun])
		return MyData
	def PopulateTemplates(self,MyData=''):
		print("PopulateTemplates")
		if MyData:
			pass
		else: MyData=self.EMAPIHandler.GetAllTemplates()
		for obj in MyData:
			self.Templates.AddObjects([Template(**obj)])
		return MyData
	def PopulateNetworks(self,MyData=''):
		print("PopulateNetworks")
		if MyData:
			pass
		else:
			Device_IDs = []
			for D in self.Devices:
				Device_IDs.append(D.device_id)
			MyData=self.EMAPIHandler.GetAllNetworks(Device_IDs)
		for d in MyData:
			device_id=d["device_id"]
			mynode=self.Nodes.FindObjects({'device_id':device_id})[0]
			for n in d["networks"]:
					if type(n) is dict:
						MyNetwork=n
						#MyNetwork["device_id"]=device_id
						#pprint.pprint(MyNetwork)
						NewNetwork=Network(**MyNetwork)
						#self.Networks.AddObjects([NewNetwork])
						mynode.Networks.AddObjects([NewNetwork])
		return(MyData)
	def PopulateAppliedTemplates(self,MyData=''):
		print("PopulateAppliedTemplates")
		for o in self.Nodes:
			o.PopulateAppliedTemplates()
		return()
		if MyData:
			pass
		else:
			Device_IDs = []
			for D in self.Devices:
				Device_IDs.append(D.device_id)
				MyData=self.EMAPIHandler.appliedTemplatelist(D.device_id)[1]
				mynode=self.Nodes.FindObjects({'device_id':D.device_id})[0]
				for n in MyData["results"]:
					if type(n) is dict:
						MyAppliedTemplate=n
						mynode.AppliedTemplates.AddObjects([AppliedTemplate(**MyAppliedTemplate)])
		return(MyData)
	def PopulateClients(self,MyData=[]):
		print("PopulateClients")
		if MyData:
			pass
		else:
			for o in self.Nodes:
				o.PopulateClients()
			return()
			Device_IDs = []
			for D in self.Devices:
				Device_IDs.append(D.device_id)
				ClientsData=self.EMAPIHandler.clientList(D.device_id)[1]["data"]
				#{'device_id':D.device_id,'data':ClientsData}
				mynode=self.Nodes.FindObjects({'device_id':D.device_id})[0]
				#print(mynode.Device.device_model)
				for ct in ClientsData.keys():
					#print(ct)
					for interface in ClientsData[ct].keys():
						for ssid in ClientsData[ct][interface].keys():
							for mac in ClientsData[ct][interface][ssid].keys():
								ClientDetails = {}
								for detail in ClientsData[ct][interface][ssid][mac][0].keys():
									ClientDetails[detail]=ClientsData[ct][interface][ssid][mac][0][detail]
								ClientDetails['mac']=mac
								if 'connected_clients_eth_info' == ct:
									ClientDetails['interface']=ssid
								else:
									ClientDetails['interface']=interface
								ClientDetails['ssid']=ssid
								ClientDetails['method']=ct
								ClientDetails['device_id']=D.device_id
								MyClient=Client(**ClientDetails)
								mynode.Clients.AddObjects([MyClient])

	def Populate(self,MyData=''):
		print("Populate")
		if MyData:
			self.PopulateDevices(ReadfromJSON("devices.json"))
			self.PopulateTunnels(ReadfromJSON("tunnels.json"))
			self.PopulateTemplates(ReadfromJSON("templates.json"))
			self.PopulateNetworks(ReadfromJSON("networks.json"))
		else:
			self.PopulateDevices()
			#self.PopulateTunnels()
			self.PopulateTemplates()
			#self.PopulateNetworks()
		#self.PopulateClients()
		self.PopulateAppliedTemplates()
	def ApplyIPPTfromCSV(self,filename):
		MyData=ReadfromCSV(filename)
		base_template_schema_json={
			"lanConfig": [
				{
					"id": "0S1N77HTQ",
					"dns1": "",
					"dns2": "",
					"name": "Default",
					"zone": "lan",
					"macacl": "",
					"subnet": "",
					"vlanID": "",
					"gateway": "",
					"netmask": "",
					"protocol": "ippt",
					"auth_port": "",
					"dnsServer": "useDNSFromISP",
					"ipAddress": "",
					"isdeleted": "0",
					"leaseTime": "1440",
					"dhcpServer": "0",
					"dnsAddress": "",
					"endAddress": "",
					"masquerade": "1",
					"auth_secret": "",
					"auth_server": "",
					"is_loopback": "0",
					"loopback_id": "",
					"networkName": "lan",
					"bridgeStatus": "0",
					"startAddress": "",
					"interfaceName": "TBD",
					"no_of_subnets": "200",
					"802_1x_enabled": "0",
					"is_auto_increment": "0",
					"staticRouteDestinationIP": "",
					"is_usb_enable": 0
				}
			],
			"wanConfig": [
				{
					"id": "BABX3XNWC",
					"name": "Cellular",
					"zone": "wan",
					"subnet": "",
					"gateway": "",
					"netmask": "",
					"protocol": "dhcpclient",
					"auth_port": "",
					"ipAddress": "",
					"isdeleted": "0",
					"dhcpClient": "1",
					"dnsAddress": "",
					"auth_secret": "",
					"auth_server": "",
					"is_loopback": "0",
					"loopback_id": "",
					"networkName": "wan",
					"bridgeStatus": "0",
					"interfaceName": "rmnet_data0",
					"802_1x_enabled": "0"
				}
			],
			"reservations": []
		}
		for j in range(1,len(MyData)):
			mychanges=[]
			row = MyData[j]
			#IMEI mode
			mynode=self.Nodes.FindObjects({'device_imei':row[0]})[0]
			#MAC mode
			#mynode=self.Nodes.FindObjects({'device_mac':row[0]})[0]
			device_id=mynode.device_id
			macacl=row[1]
			mylen=len(row)
			route=""
			for i in range(3,mylen):
				if i == 3:route=row[i]
				else: route=route+','+row[i]
			template_schema_json=base_template_schema_json
			if row[2] == "Eth" or row[2] == "eth":template_schema_json["lanConfig"][0]["interfaceName"] = "eth0"
			template_schema_json["lanConfig"][0]["staticRouteDestinationIP"]=route
			if macacl: template_schema_json["lanConfig"][0]["macacl"]=macacl
			payload={"template_id": "16"}
			payload["device_id"]=[device_id]
			payload["template_schema_json"]=template_schema_json
			#pprint.pprint(payload)
			#pprint.pprint(payload)
			for template in mynode.AppliedTemplates:
				if template.template_type=='NetworkConfiguration':
					if template.template_schema_json["lanConfig"][0]["staticRouteDestinationIP"]==payload["template_schema_json"]["lanConfig"][0]["staticRouteDestinationIP"]:
						print("Looks good! Not making any DMZ subnet changes to",row[0])
					elif template.template_schema_json["lanConfig"][0]["interfaceName"]==payload["template_schema_json"]["lanConfig"][0]["interfaceName"]:
							print("Also looks good! Not making any interface changes to",row[0])
					else:
						myoutput=self.ApplyTemplate(json.dumps(payload))
						pprint.pprint(myoutput)
						mychanges.append(myoutput)
			myfilename="ApplyIPPTfromCSV."+str(time.time())+".txt"
			print("Outputting: "+myfilename)
			WritetoJSON(mychanges,myfilename)
			#apply template to modem based off modem
class Node():
	def __init__(self,Parent,MyDevice):
		self.Device=MyDevice
		self.device_id=self.Device.device_id
		self.device_mac=self.Device.device_mac
		self.device_imei=self.Device.device_imei
		self.Networks=ObjectList()
		self.Tunnels=ObjectList()
		self.StaticRoutes=ObjectList()
		self.Clients=ObjectList()
		self.OSPFConfiguration=OSPFConfiguration()
		self.AppliedTemplates=ObjectList()
		self.Parent=Parent
	#template_type : 'FirewallConfiguration', 'BGPConfiguration', 'TriggerConfiguration', 'QoSConfiguration', 'WANConfiguration', 'NetworkConfiguration', 'SystemConfiguration', 'StaticRoute', 'WiFiConfiguration', 'OSPFConfiguration', 'DeviceProvision'
	def PopulateClients(self,MyData=[]):
		print("PopulateClients",self.device_id)
		if MyData:
			pass
		else:
			ClientsData=self.Parent.EMAPIHandler.clientList(self.device_id)[1]["data"]
			mynode=self
			for ct in ClientsData.keys():
				for interface in ClientsData[ct].keys():
					for ssid in ClientsData[ct][interface].keys():
						for mac in ClientsData[ct][interface][ssid].keys():
							ClientDetails = {}
							for detail in ClientsData[ct][interface][ssid][mac][0].keys():
								ClientDetails[detail]=ClientsData[ct][interface][ssid][mac][0][detail]
							ClientDetails['mac']=mac
							if 'connected_clients_eth_info' == ct:
								ClientDetails['interface']=ssid
							else:
								ClientDetails['interface']=interface
								ClientDetails['ssid']=ssid
							ClientDetails['method']=ct
							#ClientDetails['device_id']=self.device_id
							MyClient=Client(**ClientDetails)
							mynode.Clients.AddObjects([MyClient])
	def PopulateAppliedTemplates(self,MyData=''):
		print("PopulateAppliedTemplates",self.device_id)
		if MyData:
			pass
		else:
			MyData=self.Parent.EMAPIHandler.appliedTemplatelist(self.  device_id)[1]
			mynode=self 
			for n in MyData["results"]:
				if type(n) is dict:
					MyAppliedTemplate=n
					mynode.AppliedTemplates.AddObjects([AppliedTemplate(**MyAppliedTemplate)])
		return(MyData)
	def MapNetworks(self):
		for n in self.Parent.Networks:
			if n["device_id"] == self.Device.device_id:
				self.Networks.AddObjects([n])	
	def Serialize(self):
		mydump={}
		mydump["Device"]=self.Device.Serialize()
		mydump["Networks"]=self.Networks.Serialize()
		mydump["Tunnels"]=self.Tunnels.Serialize()
		mydump["Clients"]=self.Clients.Serialize()
		mydump["StaticRoutes"]=self.StaticRoutes.Serialize()
		mydump["AppliedTemplates"]=self.AppliedTemplates.Serialize()
		return(mydump)
	def ApplyTemplate(self,template,template_schema_json):
		if template == "OSPF":
			OSPF={
					"template_id": 217,
					"device_id": [self.device_id],"template_schema_json": template_schema_json
				}
			output = self.Parent.ApplyTemplate(json.dumps(OSPF))
			return(output)
		elif template == "IPPT":
			IPPT={
					"template_id": 13,
					"device_id": [self.device_id],"template_schema_json": template_schema_json
				}
			output = self.Parent.ApplyTemplate(json.dumps(IPPT))
			return(output)
		else:
			pass
	def AddStaticRoute(self,**kwargs):
		NewStaticRoute=StaticRoute(**kwargs)
		self.StaticRoutes.AddObjects([NewStaticRoute])
	def GetOperationApplyStatus(self):
		pass
class Device():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['device_id', 'device_name', 'device_model', 'device_serial', 'hostname', 'device_firmware_version', 'device_model_number', 'device_imei', 'device_mac', 'tenant_id', 'is_approved', 'is_headendcpe', 'platform', 'device_eth_wan_ip', 'device5g_interface_ip', 'device_control_tunnel_ip', 'device_wg_pubkey', 'device_md5', 'device_username', 'device_password', 'device_status', 'device_configured_date', 'created_by', 'created_date', 'updated_by', 'updated_date', 'device_location', 'device_delete_status', 'z_host_id', 'z_template_id', 'zabbix_template_version', 'eth_port_status', 'is_fixed_ip', 'device_public_data_key', 'is_deleted', 'guacamole_identifier', 'supported_templates', 'is_pinned', 'pf_root_password', 'modem_version', 'is_ippt', 'is_hub', 'group_name']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
	def getDeviceDetails(self):
		pass
class Client():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ["mac","device_name","device_ip","rx_bytes","tx_bytes","method","interface","ssid"]:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
class Template():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['id', 'template_id', 'template_name', 'template_type', 'device_model', 'hub_device_mac', 'template_desc', 'collection_version', 'fw_version', 'template_schema_json', 'created_by', 'created_date', 'updated_by', 'updated_date', 'device_attached', 'default_type', 'template_order', 'is_factory_temp', 'is_deleted', 'template_version']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
class AppliedTemplate():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['template_operation_id', 'device_id', 'template_id', 'hub_and_spoke_uuid', 'template_operation_type', 'template_schema_json', 'created_by', 'created_date', 'template_name', 'tunnel_id', 'template_type', 'template_order', 'template_operation_status', 'operation_id', 'is_deleted', 'state', 'default_type', 'device_model', 'collection_version', 'fw_version', 'template_version']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)	
class Network():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['device_id','name', 'interfaceName', 'networkName', 'networkTunnelLink', 'remote_deviceName', 'remote_networkTunnelLink', 'remote_tunnelIp', 'network_zone', 'ip_address', 'subnet', 'protocol', 'dhcpServer', 'netmask', 'gateway', 'DNS', 'allowedIp', 'bridgeStatus', 'VLAN', 'dhcp_range', 'leaseTime', 'Bridge_name', 'ssid', '802_1x_enabled', 'is_auto_increment', 'VLAN ID', 'dhcpClient']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
class OSPFConfiguration():
	def __init__(self,**kwargs):
		self.areaDetails=[]
		self.distanceConfiguration={
            "interAreaDistance": "110",
            "intraAreaDistance": "110",
            "externalRouteDistance": "110"
        }
		self.redistribution={}
		self.redistribution["protocol"]=""
		for key, value in kwargs.items():
			if key in ['redistribution','areaDetails','distanceConfiguration']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
	def SetDistances(self,**kwargs):
		for key, value in kwargs.items():
			distanceConfiguration={}
			if key in ['interAreaDistance', 'intraAreaDistance', 'externalRouteDistance']:
				setattr(distanceConfiguration, key, value)
				self.distanceConfiguration = distanceConfiguration
	def AddArea(self,mydict):
		self.areaDetails.append(mydict)
	def AddRedistribution(self,protocols=[]):
		for protocol in protocols:
			if protocol in ['bgp','connected','static','kernel']:
				if protocol not in self.redistribution["protocol"]:
					if self.redistribution["protocol"] == '': self.redistribution["protocol"]=protocol
					else:
						self.redistribution["protocol"]=self.redistribution["protocol"]+','+protocol
	def GeneratePayload(self):
		template_schema_json={}
		template_schema_json["distanceConfiguration"]=self.distanceConfiguration
		template_schema_json["areaDetails"]=self.areaDetails
		template_schema_json["redistribution"]=self.redistribution
		return(template_schema_json)


class StaticRoute():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['type', 'metric', 'target', 'gateway', 'isvtysh', 'netmask', 'network', 'isdeleted', 'routename']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
class Tunnel():
	def __init__(self,**kwargs):
		for key, value in kwargs.items():
			if key in ['tunnel_id', 'tunnel_name', 'device_A_mac', 'device_B_mac', 'device_A_allowedIPs', 'device_B_allowedIPs', 'device_A_endpoint', 'device_B_endpoint', 'device_A_private_ip', 'device_B_private_ip', 'A_publicKey', 'B_publicKey', 'device_a_add_zone_in_firewall', 'device_b_add_zone_in_firewall', 'device_a_add_bgp_in_tunnel', 'device_b_add_bgp_in_tunnel', 'device_A_wg_interface', 'device_B_wg_interface', 'device_A_port', 'device_B_port', 'device_A_tunnel_link', 'device_B_tunnel_link', 'tunnel_keep_alive_status', 'tunnel_keep_alive_interval', 'tunnel_split_status', 'tunnel_WAN', 'created_by', 'created_date', 'updated_by', 'updated_date', 'tunnel_interface_name', 'tunnel_latency', 'tunnel_status', 'drop_rate_in', 'drop_rate_out', 'tunnel_data_usage', 'device_A_host_id', 'device_B_host_id', 'device_A_IsHub', 'device_B_IsHub', 'template_operation_id', 'group_id', 'tunnel_type', 'device_a_status', 'device_b_status']:
				setattr(self, key, value)
	def Serialize(self):
		return(self.__dict__)
def WritetoJSON(data,filename):
	myfile=open(filename,"w")
	myfile.write(json.dumps(data))
def ReadfromJSON(filename):
	myfile=open(filename,"r")
	mydata=json.loads(myfile.read())
	return(mydata)
def ReadfromFile(filename):
	myfile=open(filename,"r")
	mydata=myfile.read()
	return(mydata)
def GetPayload(filename="payload.json"):
	payload=ReadfromFile(filename)
	return(payload)
def ReadfromCSV(filename):
	myout=[]
	mydata=ReadfromFile(filename)
	for row in mydata.split('\n'):
		myrow=[]
		for column in row.split(","):
			myrow.append(column)
		myout.append(myrow)
	return(myout)
def ApplyTemplate():
	pass
	#data=MyEMHandler.GetAllDevicesDetails()
	#WritetoJSON(data,"mydata.json")
	#MyOutput=MyEMHandler.getDeviceOperations()
	#MyPayload=GetPayload(configfile=MyFile)
	#pprint.pprint(MyPayload)
	#exit()
	#MyOutput=MyEMHandler.applyTemplate(MyPayload)
	#pprint.pprint(MyOutput)
	#MyUUID=MyOutput[1]["data"][0]['device_operation_uuid'] #[{'device_operation_uuid': '7b030c9d-28f3-4ec2-9002-561b9bd7457e', 'device_id': 89, 'template_id': 216}]
	#MyBreak=False
	#while True:
	#	#getDeviceOperations
	#	MyNewOutput=MyEMHandler.getDeviceOperations()
	#	for obj in MyNewOutput[1]["results"]:
	#		if MyUUID==obj["operation_uuid"]:
	#			print(obj["remarks"])
	#			if 'command - successful'==obj["remarks"]:
	#				MyBreak=True
	#				break
	#		else: pass
	#	if MyBreak: break
	#	#MyNewOutput[1]["results"]	  
	#	time.sleep(10)

def ListDevices(data):
		for obj in data:
			print("")
			#for k in obj.keys():
			#		print("\t{}:{}".format(k,obj[k]))

if __name__ == "__main__":  
	pass