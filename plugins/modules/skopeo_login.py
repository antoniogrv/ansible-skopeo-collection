# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: skopeo_login

short_description: Perform an authentication attemp against a target registry

version_added: "1.0.0"

description: 
    - Performs an authentication attemp against a target container registry using Skopeo.
    - Please note that additional output may be returned (e.g. stdout_lines, stderr_lines).

options:
    registry:
        description: A target container registry, either public or private, to authenticate to.
        required: true
        type: str
    username:
        description: Username to authenticate to the container registry with.
        required: true
        type: str
    password:
        description: Password to authenticate to the container registry with.
        required: true
        type: str
    tls_verify:
        description: Enables or disables TLS/HTTPS verification.
        required: false
        default: true
        type: bool
    verbose:
        description: Enables or disables verbose output on STDOUT.
        required: false
        default: false
        type: bool

author:
    - Antonio Gravino (@antoniogrv)
'''

EXAMPLES = r'''
- name: Perform an authentication attempo towards a container registry
  local.skopeo.skopeo_login:
    registry: quay.dev
    username: my_username
    password: my_password

- name: Perform an authentication attempo towards a container registry without TLS verification
  local.skopeo.skopeo_login:
    image_name: quay.dev
    username: my_username
    password: my_password
    tls_verify: false
'''

RETURN = r'''
changed:
    description: Always returns "false", as authenticating to a registry doesn't persist any change.
    type: bool
    returned: always
    sample: false
return_code:
    description: Return code of the Skopeo execution. Defaults to 0 in case of success.
    type: int
    returned: always
    sample: 0
'''

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.skopeo_command import SkopeoCommand


def run_module():
    OPERATION: str = "login"

    module_args = dict(
        registry=dict(type='str', required=True),
        tls_verify=dict(type='bool', required=False, default=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        verbose=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        return_code=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    skopeo_command_args = [
        OPERATION,
        f"--username={module.params['username']}",
        f"--password={module.params['password']}",
        f"--tls-verify={str(module.params['tls_verify'])}",
        f"--verbose={str(module.params['verbose'])}"
    ]

    skopeo_command_args.append(module.params['registry'])

    skopeo = SkopeoCommand(command=skopeo_command_args)

    result['return_code'] = skopeo.get_return_code()
    result['stdout_lines'] = skopeo.get_stdout()
    result['stderr_lines'] = skopeo.get_stderr()
    
    if module.check_mode or skopeo.failed():
        module.fail_json(skopeo.get_stderr(), **result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    run_module()