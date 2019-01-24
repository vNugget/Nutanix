#!/usr/bin/env python3

import requests
import urllib3
import ApiTools
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
####change this according to your env####
pcLogin = "admin"
pcPasswd = "unknown"
pcBaseURL = "https://x.x.x.x:9440"
srcVM = "VM1"
dstVM = "VM2"
######


mySession = requests.Session()
headers = {'Content-Type': 'application/json; charset=utf-8'}
srcVMInfo = mySession.get(pcBaseURL + "/PrismGateway/services/rest/v2.0/vms/?filter=vm_name%3D%3D"+srcVM+"&include_vm_disk_config=true" ,auth=(pcLogin, pcPasswd),verify=False)
result = srcVMInfo.json()
masterUuid = []
ApiTools.jsonScan(result,'uuid',masterUuid)
print("Master VM UUID = {}".format(masterUuid[0]))
#
masterDiskUuid = []
ApiTools.jsonScan(result,'vmdisk_uuid',masterDiskUuid)
print("Master VM second disk UUID = {}".format(masterDiskUuid[2]))
#
dstVMInfo = mySession.get(pcBaseURL + "/PrismGateway/services/rest/v2.0/vms/?filter=vm_name%3D%3D"+dstVM ,auth=(pcLogin, pcPasswd),verify=False)
result = dstVMInfo.json()


#dstVMUuid = result['entities'][0]['uuid']
#print("Slave VM UUID = {}".format(dstVMUuid))

#print("clone the disk")
data = {
  "disks": [
    {
      "vmDiskClone": {
        "vmDiskUuid": masterDiskUuid[2]
      }
    }
  ]
}
#print(data)
#result = mySession.post(pcBaseURL + "/api/nutanix/v0.8/vms/"+dstVMUuid+"/disks/",json=data,headers=headers,auth=(pcLogin, pcPasswd),verify=False)
#print(result.text)

