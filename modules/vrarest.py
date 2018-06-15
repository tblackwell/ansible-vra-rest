#!/usr/bin/python

SOCKET_TIMEOUT = 30
DEFAULT_TENANT = 'vsphere.local'

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: vra7rest

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
  vrarest:
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

def main():
    # Define the parameters that a user can pass into this module.
    module_args = dict(
        host=dict(type='str', required=True),
        rest_method=dict(type='str', required=True, choices=['get_bearer_token', 'get_catalog_items', 'get_blueprint_template', 'submit_blueprint_request', 'check_blueprint_status']),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        vm_template=dict(type='str', required=False, default=""),
        tenant=dict(type='str', required=False, default=DEFAULT_TENANT),
        token=dict(type='str', required=False),
        catalog_item_id=dict(type='str', required=False, default=""),
        validate_certs=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        response_content='',
        response_json={},
        token='',
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
    rest_method = module.params['rest_method']
    username = module.params['username']
    password = module.params['password']
    vm_template = module.params['vm_template']
    tenant = module.params['tenant']
    token = module.params['token']
    catalog_item_id = module.params['catalog_item_id']
    body_format = 'json'
    body = ''
    body_json = {}

    if rest_method == 'get_bearer_token':
        method = 'POST'
        url = 'https://' + host + '/identity/api/tokens'
        headers = {'Accept':'application/json',
                   'Content-Type':'application/json'}
        body_json = {'username': username,
                     'password': password,
                     'tenant': tenant}
        body = json.dumps(body_json)
    elif rest_method == 'get_catalog_items':
        method = 'GET'
        url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItemViews'
        headers = {'Accept':'application/json',
                   'Content-Type':'application/json',
                   'Authorization':'Bearer ' + token}
    elif rest_method == 'get_blueprint_template':
        method = 'GET'
        url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItems/' + catalog_item_id + '/requests/template'
        headers = {'Accept':'application/json',
                   'Authorization':'Bearer ' + token}
    elif rest_method == 'submit_blueprint_request':
        method = 'POST'
        url = 'https://' + host + '/catalog-service/api/consumer/entitledCatalogItems/' + catalog_item_id + '/requests'
        headers = {'Accept':'application/json',
                   'Content-Type':'application/json',
                   'Authorization':'Bearer ' + token}
        body = vm_template

        # These replace statements clean up the raw template string to make it
        # suitable for parsing by the Python JSON parser.  This ensures that the
        # template can be parsed into a JSON object so that new values can be
        # placed into the object based on the user's desired configuration for
        # the resulting VM(s).
        body = body.replace("None", "null")
        body = body.replace("\'", "\"")
        body = body.replace("False", "false")
        body = body.replace("True", "true")

    output = {'url': url,
              'body': body,
              'vm_template': vm_template,
              'catalog_item_id': catalog_item_id}

    # Make the request
    response, info = fetch_url(module,
                               url,
                               data=body,
                               headers=headers,
                               method=method,
                               timeout=SOCKET_TIMEOUT)

    # Retrieve the response content.
    if response is None:
        response_content = "{ 'Response': 'Is Null'}"
        response_json = {'Response': 'Is Null'}
    else:
        response_content = response.read()
        response_json = json.loads(response_content)

    # Parse the content into a JSON object.
    #response_json = json.loads(response_content)

    # Retrieve the result parameters from the response.
    if rest_method == 'get_bearer_token':
        result['token'] = response_json["id"]
        #print "token", result['token']
    elif rest_method == 'get_catalog_items':
        result['response_json'] = response_json
        result['response_content'] = response_content
        #print 'response_content', response_content
    elif rest_method == 'get_blueprint_template':
        result['response_json'] = response_json
        result['response_content'] = response_content
        #print 'response_content', response_content
    elif rest_method == 'submit_blueprint_request':
        result['response_json'] = response_json
        result['response_content'] = response_content
        #print 'response_content', response_content
    elif rest_method == 'check_blueprint_status':
        result['response_json'] = response_json
        result['response_content'] = response_content
        #print 'response_content', response_content

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

    result['output'] = json.dumps(output)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
