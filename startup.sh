#!/bin/bash

# Check if sudo privileges are available
if sudo -l &>/dev/null; then
    USER_UID=$(id -u)
    USER_GID=$(id -g)

    sudo chown -R $USER_UID:$USER_GID /var/run/docker.sock
    sudo chown -R $USER_UID:$USER_GID /data
    sudo wait-for-it.sh db:5432
fi

quetz init-db /data
quetz start /data --port 8000 --host 0.0.0.0 --proxy-headers --reload --log-level=trace
