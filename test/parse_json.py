#!/usr/bin/python

import json

def id_generator(dict_var):
      for k, v in dict_var.items():
            if k == "id":
                 yield v
            elif isinstance(v, dict):
                 for id_val in id_generator(v):
                       yield id_val

json_data = '{"name":"John","age":30,"cars": {"car1":"Ford","car2":"BMW","car3":"Fiat"}}'
python_obj = json.loads(json_data)
print python_obj["name"]
print python_obj["age"]

json_example_file = open('json_example.txt', 'r+')
json_example_raw = json_example_file.read()
json_example_file.close()

print "JSON Example Raw: ", json_example_raw
print ""
print ""

json_example_obj = json.loads(json_example_raw)
print "JSON Example Parsed", json_example_obj
print ""
print ""

json_template_file = open('vm_template_raw.txt', 'r+')
json_template_raw = json_template_file.read()
json_template_file.close()

print "JSON Template Raw: ", json_template_raw
print ""
print ""

# Remoe the None's
json_template_without_nones = json_template_raw.replace("None", "null")
json_template_without_nones = json_template_without_nones.replace("\'", "\"")
#json_template_without_nones = json_template_without_nones.replace("}}}}", "} } } }")
json_template_without_nones = json_template_without_nones.replace("False", "false")
json_template_without_nones = json_template_without_nones.replace("True", "true")
print "JSON Template Without None's: ", json_template_without_nones
print ""
print ""

json_template_partial = '{"requestedFor": "jason@corp.local", "description": null, "reasons": null, "type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest", "catalogItemId": "e5dd4fba-45ed-4943-b1fc-7f96239286be", "businessGroupId": "29a02ed9-7e63-4c77-8a15-c930afb0e3d8", "data": {"_leaseDays": null, "_archiveDays": 5, "CentOS_6.3": {"classId": "Blueprint.Component.Declaration", "componentTypeId": "com.vmware.csp.component.cafe.composition", "typeFilter": "CentOS63*CentOS_6.3", "componentId": null, "data": {"_hasChildren": False, "datacenter_location": null, "security_tags": [], "reservation_policy": null, "security_groups": [], "guest_customization_specification": "CentOS", "nics": null, "storage": 3, "os_arch": "x86_64", "_cluster": 1, "os_version": null, "memory": 512, "max_per_user": 0, "description": "Basic IaaS CentOS Machine", "machine_prefix": null, "disks": [{"classId": "Infrastructure.Compute.Machine.MachineDisk", "componentTypeId": "com.vmware.csp.iaas.blueprint.service", "typeFilter": null, "componentId": null, "data": {"capacity": 3, "custom_properties": null, "storage_reservation_policy": "", "userCreated": False, "volumeId": 0, "initial_location": "", "label": "Hard disk 1", "is_clone": True, "id": 1450725224066}}], "_allocation": {"classId": "Infrastructure.Compute.Machine.Allocation", "componentTypeId": "com.vmware.csp.iaas.blueprint.service", "typeFilter": null, "componentId": null, "data": {"machines": null}}, "max_network_adapters": -1, "max_volumes": 60, "property_groups": null, "os_type": "Linux", "os_distribution": null, "cpu": 1}}, "_number_of_instances": 1, "corp192168110024": {"classId": "Blueprint.Component.Declaration", "componentTypeId": "com.vmware.csp.component.cafe.composition", "typeFilter": "CentOS63*corp192168110024", "componentId": null, "data": {"_hasChildren": False} } } }'

json_template_1 = '{"requestedFor": "jason@corp.local", "description": null, "reasons": null, "type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest", "catalogItemId": "e5dd4fba-45ed-4943-b1fc-7f96239286be", "businessGroupId": "29a02ed9-7e63-4c77-8a15-c930afb0e3d8", "data": {"_leaseDays": null, "_archiveDays": 5, "CentOS_6.3": {"classId": "Blueprint.Component.Declaration", "componentTypeId": "com.vmware.csp.component.cafe.composition", "typeFilter": "CentOS63*CentOS_6.3", "componentId": null, "data": {"_hasChildren": False, "datacenter_location": null, "security_tags": [], "reservation_policy": null, "security_groups": [], "guest_customization_specification": "CentOS", "nics": null, "storage": 3, "os_arch": "x86_64", "_cluster": 1, "os_version": null, "memory": 512, "max_per_user": 0, "description": "Basic IaaS CentOS Machine", "machine_prefix": null} } } }'

json_template_2 = '{"requestedFor": "jason@corp.local", "description": null, "reasons": null, "type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest", "catalogItemId": "e5dd4fba-45ed-4943-b1fc-7f96239286be", "businessGroupId": "29a02ed9-7e63-4c77-8a15-c930afb0e3d8", "data": {"_leaseDays": null, "_archiveDays": 5, "CentOS_6.3": {"classId": "Blueprint.Component.Declaration", "componentTypeId": "com.vmware.csp.component.cafe.composition", "typeFilter": "CentOS63*CentOS_6.3", "componentId": null, "data": {"_hasChildren": False, "datacenter_location": null} } } }'

json_template_3 = '{"requestedFor": "jason@corp.local", "description": null, "reasons": null, "type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest", "catalogItemId": "e5dd4fba-45ed-4943-b1fc-7f96239286be", "businessGroupId": "29a02ed9-7e63-4c77-8a15-c930afb0e3d8", "data": {"_leaseDays": null, "_archiveDays": 5, "CentOS_6.3": {"classId": "Blueprint.Component.Declaration", "componentTypeId": "com.vmware.csp.component.cafe.composition", "typeFilter": "CentOS63*CentOS_6.3", "componentId": null} } }'

json_template_4 = '{"requestedFor": "jason@corp.local", "description": null, "reasons": null, "type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest", "catalogItemId": "e5dd4fba-45ed-4943-b1fc-7f96239286be", "businessGroupId": "29a02ed9-7e63-4c77-8a15-c930afb0e3d8"}'

json_template_5 = "{'requestedFor': 'jason@corp.local', 'description': null, 'reasons': null, 'type': 'com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest', 'catalogItemId': 'e5dd4fba-45ed-4943-b1fc-7f96239286be', 'businessGroupId': '29a02ed9-7e63-4c77-8a15-c930afb0e3d8'}"

print "JSON Template Partial: ", json_template_2
print ""
print ""

json_template_obj = json.loads(json_template_without_nones)

print "JSON Template Parsed", json_template_obj
print ""
print ""


#print("Raw JSON: ", raw_json)

#json_with_nulls = raw_json.replace("None", "null")

#print("JSON with nulls: ", json_with_nulls)

#parsed_json = json.loads(json_with_nulls)

#print("JSON object: ", parsed_json)
