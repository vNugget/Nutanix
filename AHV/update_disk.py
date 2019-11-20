
import requests
import json
import urllib3
import argparse


ap = argparse.ArgumentParser(description='Script used to exapnd a disk attached to a VM running on AHV node')
# Add the arguments to the parser
ap.add_argument("-u", dest="pe_url", required=True, help="url for Prism Element, ex: https://1.1.1.1:9440")
ap.add_argument("-l", dest="login", required=True, help="PE login")
ap.add_argument("-p", dest="password", required=True, help="PE password")
ap.add_argument("-v", dest="vm", required=True, help="VM name")
ap.add_argument("-i", dest="index", default=1, help="Disk index, default: 1 (second disk)")
ap.add_argument("-s", dest="size", required=True, help="new size in bytes")
args = ap.parse_args()

##########
vm_name = args.vm
prism_url = args.pe_url
prism_login = args.login
prism_password = args.password
new_vdisk_size = args.size #8589934592 # in bytes
vdisk_index = args.index
########
headers = { 'content-type': "application/json" }
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

get_vm_url = prism_url + "/api/nutanix/v2.0/vms/?filter=vm_name%3D%3D"+ vm_name +"&include_vm_disk_config=true"
response = requests.request("GET", get_vm_url,auth=(prism_login, prism_password), headers=headers,verify=False)
vm = response.json()
vdisk_uuid = vm['entities'][0]['vm_disk_info'][1]['source_disk_address']['vmdisk_uuid']
container_uuid = vm['entities'][0]['vm_disk_info'][1]['storage_container_uuid']
vm_uuid = vm['entities'][0]['uuid']

print("vm uuid: {}\nvdisk uuid: {} \ncontainer uuid: {}".format(vm_uuid,vdisk_uuid,container_uuid))

update_vdisk_payload = {
  "vm_disks": [
    {
      "disk_address": {
        "vmdisk_uuid": vdisk_uuid,
        "device_index": vdisk_index,
        "device_bus": "scsi"
      },
      "flash_mode_enabled": False,
      "is_cdrom": False,
      "is_empty": False,
      "vm_disk_create": {
        "storage_container_uuid": container_uuid,
        "size": new_vdisk_size
      }
    }
  ]
}

update_vm_url = prism_url + "/PrismGateway/services/rest/v2.0/vms/" + vm_uuid + "/disks/update"
response = requests.request("PUT", update_vm_url,auth=(prism_login, prism_password),json=update_vdisk_payload, headers=headers,verify=False)
print(response.status_code)

