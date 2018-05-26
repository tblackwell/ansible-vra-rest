#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jsonmodify

short_description: A module that sets values in a JSON object.

version_added: "2.4"

description:
    - This module provides the capability of setting a value into a given JSON
      via a supplied path to that value.

options:
    json:
        description:
            - The JSON object that will receive the new value.
        required: true
    json_path:
        description:
            - The path to the attribute to change.  The path uses the '/' to
              separate distinct levels in the JSON object.
        required: true
    new_value:
        description:
            - The new value to set into the JSON object.
        required: true

author:
    - Todd Blackwell (@vmware.com)
'''

EXAMPLES = '''
# Fill in later
- name: Get a Bearer Token
  vra7rest:
    host: vra-01a.corp.local
    rest_method: get_bearer_token
    username: jason
    password: VMware1!
    tenant: vsphere.local
'''

RETURN = '''
Nothing: The JSON object passed into this function is modified directly, so no
         return object is necessary.
'''

import json

from ansible.module_utils.basic import AnsibleModule

# A recursive function that sets the specified value into the given JSON object.
#
# TODO: Modify this function so that if the path element is a number, then treat
#       the outer-most JSON object as a list with the number being the index.
def set_json_value(json, path_list, new_value):

    if len(path_list) > 1:
        outer_most_path_element = path_list.pop(0)
        sub_json_object = json[outer_most_path_element]
        set_json_value(sub_json_object, path_list, new_value)
    else:
        json[path_list[0]] = new_value

# The main function that gets executed for the module.
def main():
    # Define the parameters that a user can pass into this module.
    module_args = dict(
        json=dict(type='raw', required=True),
        json_path=dict(type='str', required=True),
        new_value=dict(type='str', required=True)
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    json = module.params['json']
    json_path = module.params['json_path']
    new_value = module.params['new_value']

    # Break apart the JSON path into a list of path segments.
    path_list = json_path.split("/")

    # Call the recursive function to set the new value.
    set_json_value(json, path_list, new_value)

    output = {'modified_json': json}

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        modified_json=json,
        output=''
    )

    # If the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # Use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['json']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['json'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    #result['output'] = json.dumps(output)
    result['output'] = output

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

if __name__ == '__main__':
    main()
