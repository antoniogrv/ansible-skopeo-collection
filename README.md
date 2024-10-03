# Ansible Skopeo Collection

This repository contains an [Ansible](https://www.ansible.com/) collection that allows to perform interactive [Skopeo](https://github.com/containers/skopeo) actions within Ansible playbooks or roles. This module requires a working installation of Skopeo on the target hosts.

This may be handy when setting up private container registries, transfering images to and from airgapped environments, or obtaining [OCI](https://opencontainers.org/) information about specific images.

# Installation

Make sure you have the `ansible-galaxy` CLI installed, then run the following command:

```bash
ansible-galaxy collection install <TBA>
```

# Usage

Run `ansible-doc -l local.skopeo` in order to list availalbe modules, roles and plugins. Afterwards, run `ansible-doc -l local.skopeo.<plugin_name>` to access the documentation of the selected module.

Module | Description
---: | :---
`skopeo_login`   | Perform an authentication attemp against a target registry
`skopeo_inspect` | Inspects a container image, returning a JSON object
`skopeo_copy`    | Copies a container image from one registry to another

# Examples

```yaml
- name: Attemp to authenticate against the quay.dev private container registry
  local.skopeo.skopeo_login:
    registry: quay.dev
    username: my_username
    password: my_password

- name: Attemp to authenticate against the quay.dev private container registry without TLS verification
  local-skopeo.skopeo_login:
    image_name: quay.dev
    username: my_username
    password: my_password
    tls_verify: false

- name: Inspect a remote container image on a quay.dev private registry
  local.skopeo.skopeo_inspect:
    image_name: quay.dev/my/image:tag
    username: my_username
    password: my_password

- name: Copy a busybox image from docker.io to a quay.dev private registry
  local.skopeo.skopeo_copy:
    src_image: "docker://docker.io/busybox:1.37"
    dest_image: "docker://quay.dev/misc/busybox:1.37"
    dest_username: "my_username"
    dest_password: "my_password"
```