#!/usr/bin/python

SOCKET_TIMEOUT = 30
DEFAULT_TENANT = 'vsphere.local'
DEFAULT_MEMORY = 512
DEFAULT_CPUS = 1

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: vravm
short_description: A module that wraps the vRA 7 REST calls.
version_added: "2.4"
description:
    - This module provides a wrapper for making vRA API REST calls to a specific
      vRA instance.
options:
    host:
        description:
            - This is vRA host name.
        required: true
    rest_method:
        description:
            - The name of the REST method to call on the host.
        required: true
    username:
        description:
            - The user name to use when logging into the vRA instance to
              retrieve a bearer token.
        required: false
    password:
        description:
            - The password for the user logging into the vRA  instance to
              retrieve a bearer token.
        required: false
    vm_template:
        description:
            - The JSON blueprint template object that acts as the configuration
              for the VM to be provisioned.
        required: false
    tenant:
        description:
            - The tenant for the user making the REST call.  This will default
              to "vsphere.local".
        required: false
    token:
        description:
            - The bearer token to use with all calls other than the one to
              retrieve the bearer token.
        required: false
    catalog_item_id:
        description:
            - The ID of the catalog item that is to be the target of the method
              execution.
        required: false
author:
    - Todd Blackwell (@vmware.com)
'''

EXAMPLES = '''
# Retrieve a bearer token
- name: Get a Bearer Token
  vra7rest:
    host: vra-01a.corp.local
    rest_method: get_bearer_token
    username: jason
    password: VMware1!
    tenant: vsphere.local
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, url_argument_spec

def set_json_value(json, path_list, new_value):

    if len(path_list) > 1:
        outer_most_path_element = path_list.pop(0)
        sub_json_object = json[outer_most_path_element]
        set_json_value(sub_json_object, path_list, new_value)
    else:
        json[path_list[0]] = new_value

def main():
    # Define the parameters that a user can pass into this module.
    module_args = dict(
        host=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        tenant=dict(type='str', required=False, default=DEFAULT_TENANT),
        blueprint_name=dict(type='str', required=False),
        memory=dict(type='str', required=False, default=DEFAULT_MEMORY),
        cpu_count=dict(type='str', required=False, default=DEFAULT_CPUS
        num_of_instances=dict(type='num', required=False, default=1)
        wait_for_vm=dict(type='str', required=False, default=False),
        validate_certs=dict(type='str', required=False)
    )

    body_format = 'json'
    body = ''
    body_json = {}
    output = {'headers': '',
              'url': '',
              'bearer_token': '',
              'catalog_items': {},
              'blueprint_catalog_item_id': '',
              'blueprint_item': {},
              'blueprint_template': {},
              'response': {}}

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        result_text='',
        output=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    host = module.params['host']
    username = module.params['username']
    password = module.params['password']
    tenant = module.params['tenant']
    blueprint_name = module.params['blueprint_name']
    memory = module.params['memory']
    cpu_count = module.params['cpu_count']
    number_of_instances = module.params['num_of_instances']
    body_format = 'json'
    body = ''
    body_json = {}
    output = {'headers': '',
              'url': '',
              'bearer_token': '',
              'catalog_items': {},
              'blueprint_catalog_item_id': '',
              'blueprint_item': {},
              'blueprint_template': {},
              'response': {}}

    #===========================================================================
    # The first step is to get the bearer token.
    #===========================================================================
    method = 'POST'
    url = 'https://' + host + '/identity/api/tokens'
    headers = {'Accept':'application/json',
               'Content-Type':'application/json'}
    body_json = {'username': username,
                 'password': password,
                 'tenant': tenant}
    body = json.dumps(body_json)

    # Make the REST call to get the bearer token.
    response, info = fetch_url(module,
                               url,
                               data=body,
                               headers=headers,
                               method=method,
                               timeout=SOCKET_TIMEOUT)

    response_content = response.read()
    response_json = json.loads(response_content)
    bearer_token = response_json["id"]

    output['bearer_token'] = bearer_token

    #===========================================================================
    # Get the list of catalog items.
    #===========================================================================
    method = 'GET'
    url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItemViews'
    headers = {'Accept':'application/json',
              'Content-Type':'application/json',
              'Authorization':'Bearer ' + bearer_token}

    # Make the request
    response, info = fetch_url(module,
                               url,
                               data=body,
                               headers=headers,
                               method=method,
                               timeout=SOCKET_TIMEOUT)

    response_content = response.read()
    catalog_items = json.loads(response_content)['content']

    # Find the catalog item that matches the blueprint name passed into this
    # module.
    blueprint_item = {}
    for catalog_item in catalog_items:
        if catalog_item['name'] == blueprint_name:
            blueprint_item = catalog_item

    if blueprint_item:
        blueprint_catalog_item_id = blueprint_item['catalogItemId']

        output['blueprint_item'] = blueprint_item
        output['blueprint_catalog_item_id'] = blueprint_catalog_item_id
    else:
        raise Exception("Blueprint could not be found")

    #===========================================================================
    # Get the blueprint template using the catalog ID.
    #===========================================================================
    method = 'GET'
    url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItems/' + blueprint_catalog_item_id + '/requests/template'
    headers = {'Accept':'application/json',
               'Authorization':'Bearer ' + bearer_token}

    # Make the request
    response, info = fetch_url(module,
                               url,
                               data=body,
                               headers=headers,
                               method=method,
                               timeout=SOCKET_TIMEOUT)

    response_content = response.read()
    blueprint_template = json.loads(response_content)

    output['blueprint_template'] = blueprint_template

    #===========================================================================
    # Update the template with the new values supplied by the user.
    #===========================================================================
    blueprint_data_item_name = blueprint_name.replace(' ', '_')
    memory_path = 'data/' + blueprint_data_item_name + '/data/memory'
    cpus_path = 'data/' + blueprint_data_item_name + '/data/cpu'
    number_of_instances_path = 'data/_number_of_instances'

    memory_path_list = memory_path.split('/')
    cpus_path_list = cpus_path.split('/')
    number_of_instances_list = number_of_instances_path.split('/')

    set_json_value(blueprint_template, memory_path_list, memory)
    set_json_value(blueprint_template, cpus_path_list, cpu_count)
    set_json_value(blueprint_template, number_of_instances_list, cpu_count)

    #===========================================================================
    # Submit the modified blueprint template to provision the VM.
    #===========================================================================
    method = 'POST'
    url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItems/' + blueprint_catalog_item_id + '/requests'
    headers = {'Accept':'application/json',
               'Content-Type':'application/json',
               'Authorization':'Bearer ' + bearer_token}

    # Make the request
    response, info = fetch_url(module,
                               url,
                               data=json.dumps(blueprint_template),
                               headers=headers,
                               method=method,
                               timeout=SOCKET_TIMEOUT)

    output['response'] = response
    output['url'] = url
    output['headers'] = headers
    response_content = response.read()
    blueprint_template = json.loads(response_content)

    # If the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # Use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['host']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['host'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    result['output'] = output

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
