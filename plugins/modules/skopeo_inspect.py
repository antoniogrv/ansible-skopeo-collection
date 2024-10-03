# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: skopeo_inspect

short_description: Inspects a container image with Skopeo

version_added: "1.0.0"

description: 
    - Inspects a container image on a registry using Skopeo. Returned data is formatted as a JSON.
    - Please note that additional output may be returned (e.g. stdout_lines, stderr_lines).

options:
    image_name:
        description: | 
            Container image name, usually prefixed by a container transport protocol (e.g. docker://, oci://).
            Please refer to https://github.com/containers/skopeo/blob/main/docs/skopeo.1.md for more information.
            Example: docker://quay.io/namespace/image:tag
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

author:
    - Antonio Gravino (@antoniogrv)
'''

EXAMPLES = r'''
- name: Inspect a remote container image
  skopeo.skopeo_inspect:
    image_name: quay.dev/my/image:tag
    username: my_username
    password: my_password

- name: Inspect a remote container image without TLS verification
  skopeo.skopeo_inspect:
    image_name: quay.dev/my/image:tag
    username: my_username
    password: my_password
    tls_verify: false
'''

RETURN = r'''
changed:
    description: Always returns "false", as inspecting a container image doesn't persist any change.
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
    OPERATION: str = "inspect"

    module_args = dict(
        image_name=dict(type='str', required=True),
        tls_verify=dict(type='bool', required=False, default=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True),
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
        f"--creds={module.params['username']}:{module.params['password']}",
        f"--tls-verify={str(module.params['tls_verify'])}",
    ]

    skopeo_command_args.append(module.params['image_name'])

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