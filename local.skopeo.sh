#!/bin/env bash

export ANSIBLE_LIBRARY=./plugins/modules
export ANSIBLE_MODULE_UTILS=./plugins/module_utils

OPERATION=$1
REGISTRY_USERNAME=$2
REGISTRY_PASSWORD=$3

lint() {
	pre-commit run --all-files
}

list-docs() {
	ansible-doc -l local.skopeo
}

test_skopeo_login() {
	ansible -m skopeo_login \
    -a 'registry=quay.dev \
	username='"$REGISTRY_USERNAME"' \
	password='"$REGISTRY_PASSWORD"' \
	tls_verify=false' \
	localhost
}

test_skopeo_inspect() {
	ANSIBLE_LIBRARY=./plugins/modules \
	ANSIBLE_MODULE_UTILS=./plugins/module_utils \
		ansible -m skopeo_inspect -a \
		'image_name="docker://quay.dev/misc/busybox:1.36" \
		username='"$REGISTRY_USERNAME"' \
		password='"$REGISTRY_PASSWORD"' \
		tls_verify=false' \
		localhost
}

test_skopeo_copy() {
	ANSIBLE_LIBRARY=./plugins/modules \
	ANSIBLE_MODULE_UTILS=./plugins/module_utils \
		ansible -m skopeo_copy -a \
		'src_image=docker://docker.io/busybox:1.36 \
		dest_image=docker://quay.dev/misc/busybox:1.36 \
		dest_username='"$REGISTRY_USERNAME"' \
		dest_password='"$REGISTRY_PASSWORD"' \
		dest_tls_verify=false' \
		localhost
}

case "$1" in
    lint)
        lint
        ;;
    list-docs)
        list-docs
        ;;
    login)
        test_skopeo_login
        ;;
    inspect)
        test_skopeo_inspect
        ;;
    copy)
        test_skopeo_copy
        ;;
    *)
        echo "Comando non valido. Usa: lint, list-docs, login, inspect, copy"
        exit 1
        ;;
esac