
import requests
import json
import urllib3
import argparse

ap = argparse.ArgumentParser(description='Script used to modify network on nics for VMs running on AHV node')
# Add the arguments to the parser
ap.add_argument("-u", dest="pe_url", required=True, help="url for Prism Element, ex: https://1.1.1.1:9440")
ap.add_argument("-l", dest="login", required=True, help="PE login")
ap.add_argument("-p", dest="password", required=True, help="PE password")
ap.add_argument("-v", dest="vm", required=True, help="VM name")
ap.add_argument("-n", nargs="*", dest="vlan", required=True, help="a list of vlans name as it appear on PE")
args = ap.parse_args()

########## 
vm_name = args.vm
prism_url = args.pe_url
prism_login = args.login
prism_password = args.password
# network names, should be on the same order as nics order
nics_network = {key: None for key in args.vlan}
# list to store mac address
nics_mac = []
################ predefined vars
headers = { 'content-type': "application/json" }
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

################ network lookup
get_network_url = prism_url + "/api/nutanix/v2.0/networks/"
response = requests.request("GET", get_network_url,auth=(prism_login, prism_password), headers=headers,verify=False)
networks = response.json()
# search for network by name and store the uuid in a dict
for network in networks['entities']:
  if network['name'] in nics_network:
    print("found network {}".format(network['name']))
    nics_network.update({network['name'] : network['uuid']})

print(nics_network)
#exit(0)

################# network change 
get_vm_url = prism_url + "/api/nutanix/v2.0/vms/?filter=vm_name%3D%3D"+ vm_name +"&include_vm_nic_config=true"
response = requests.request("GET", get_vm_url,auth=(prism_login, prism_password), headers=headers,verify=False)
vm = response.json()
vm_nics = vm['entities'][0]['vm_nics']
vm_uuid = vm['entities'][0]['uuid']
counter = 0
# search for mac address and store the uuid in a list
for nics in vm_nics:
  nics_mac.append(nics['mac_address'])
  counter += 1
 
#print(nics_mac)
# update the vm nics the new network and keeping the old mac address
for vnic, (k2,network) in zip(nics_mac,nics_network.items()):
  print(vnic,network)
  update_vnics_url = prism_url + "/api/nutanix/v2.0/vms/" + vm_uuid + "/nics/" + vnic
  print("Updating nic with mac {} with {} network uuid...".format(vnic,network))
  #print(update_vnics_url)
  update_vnics_payload = {
  "nic_spec": {
    "network_uuid": network
   }
   }
  #print(update_vnics_payload)
  response = requests.request("PUT", update_vnics_url,auth=(prism_login, prism_password),json=update_vnics_payload, headers=headers,verify=False)
  print(response.status_code)
  