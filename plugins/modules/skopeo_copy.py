# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: skopeo_copy

short_description: Copies a container image from one registry to another

version_added: "1.0.0"

description: 
    - Copies a container image from a source container registry to a destination container registry.
    - If you need to copy multiple images, use an Ansible loop.
    - Please note that additional output may be returned (e.g. stdout_lines, stderr_lines).

options:
    src_image:
        description: | 
            Container image name, usually prefixed by a container transport protocol (e.g. docker://, oci://), from a source containre registry.
            Please refer to https://github.com/containers/skopeo/blob/main/docs/skopeo.1.md for more information.
            Example: docker://quay.io/namespace/image:tag
        required: true
        type: str
    dest_image:
        description: | 
            Container image name, usually prefixed by a container transport protocol (e.g. docker://, oci://), to copy into a destination containre registry.
            Please refer to https://github.com/containers/skopeo/blob/main/docs/skopeo.1.md for more information.
            Example: docker://quay.io/namespace/image:tag
        required: true
        type: str
    src_username:
        description: Username to authenticate to the source container registry with.
        required: true
        type: str
    src_password:
        description: Password to authenticate to the source container registry with.
        required: true
        type: str
    dest_username:
        description: Username to authenticate to the destination container registry with.
        required: true
        type: str
    dest_password:
        description: Password to authenticate to the destination container registry with.
        required: true
        type: str
    src_tls_verify:
        description: Enables or disables TLS/HTTPS verification against the destination registry.
        required: false
        default: true
        type: bool
    dest_tls_verify:
        description: Enables or disables TLS/HTTPS verification against the destination registry.
        required: false
        default: true
        type: bool

author:
    - Antonio Gravino (@antoniogrv)
'''

EXAMPLES = r'''
- name: Copy a container image from one registry to another, without authentication
  local.skopeo.skopeo_copy:
    src_image: docker://source.io/my/image:tag
    dest_image: docker://destination.io/my/image:tag

- name: Copy a container image from one registry to another, as an authenticated users on the destination side
  local.skopeo.skopeo_copy:
    src_image: docker://source.io/my/image:tag
    dest_image: docker://destination.io/my/image:tag
    dest_username: my_username
    dest_password: my_password

- name: Copy a container image from one registry to another, as an authenticated users on both sides and without TLS verification
  local.skopeo.skopeo_copy:
    src_image: docker://source.io/my/image:tag
    dest_image: docker://destination.io/my/image:tag
    src_username: my_username1
    src_password: my_password2
    dest_username: my_username2
    dest_password: my_password2
    src_tls_verify: false
    dest_tls_verify: false
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
    OPERATION: str = "copy"

    module_args = dict(
        src_image=dict(type='str', required=True),
        dest_image=dict(type='str', required=True),
        src_tls_verify=dict(type='bool', required=False, default=True),
        dest_tls_verify=dict(type='bool', required=False, default=True),
        src_username=dict(type='str', required=False),
        src_password=dict(type='str', required=False, no_log=True),
        dest_username=dict(type='str', required=False),
        dest_password=dict(type='str', required=False, no_log=True),
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
        f"--src-tls-verify={str(module.params['src_tls_verify'])}",
        f"--dest-tls-verify={str(module.params['dest_tls_verify'])}"
    ]

    if module.params['src_username'] and module.params['src_password']:
        skopeo_command_args.append(f"--src-creds={module.params['src_username']}:{module.params['src_password']}")

    if module.params['dest_username'] and module.params['dest_password']:
        skopeo_command_args.append(f"--dest-creds={module.params['dest_username']}:{module.params['dest_password']}")

    skopeo_command_args.extend([module.params['src_image'], module.params['dest_image']])

    skopeo = SkopeoCommand(command=skopeo_command_args)

    result['return_code'] = skopeo.get_return_code()
    result['stdout_lines'] = skopeo.get_stdout()
    result['stderr_lines'] = skopeo.get_stderr()

    if module.check_mode or skopeo.failed():
        module.fail_json(skopeo.get_stderr(), **result)
    else:
        result['changed'] = True
        module.exit_json(**result)


if __name__ == '__main__':
    run_module()