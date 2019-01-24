#!/usr/bin/env python3

import json


def jsonScan(jsonLoad, target,found):
    """Take a json object and scan it to look for specific key and get it's value.
       - target (str): is the key that we are looking for.
       - return: if found the func will append the result to the found (list) var, this var
                 should be declared before using the func
    """
    for key, value in jsonLoad.items():
        if key == target:
            #print("target {} found, value = {}".format(target,value))
            found.append(value)
        elif isinstance(value,list):
            for i in value:
                jsonScan(i,target,found)
        else:
            if isinstance(value, dict):
                jsonScan(value,target,found)
                #continue


if __name__ == "__main__":
    found = []
    with open('document.json', 'r') as f:
        json_dict = json.load(f)
        #print(distros_dict['entities'][0]['vm_disk_info'][2]['disk_address']['vmdisk_uuid'])
        jsonScan(json_dict, 'vmdisk_uuid', found)
        print(found)
