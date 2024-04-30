#!/bin/bash
if sudo -l &>/dev/null; then
    USER_UID=$(id -u)
    USER_GID=$(id -g)

    sudo chown -R $USER_UID:$USER_GID /var/run/docker.sock
    sudo chown -R $USER_UID:$USER_GID /data
    sudo chown -R $USER_UID:$USER_GID $MAMBA_ROOT_PREFIX

fi
cd /data && quetz create --create-conf /data/beta
cd /data/beta && quetz start . --port 8000 --host 0.0.0.0 --proxy-headers --reload --log-level=trace