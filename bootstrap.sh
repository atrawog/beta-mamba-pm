#!/bin/bash

if sudo -l &>/dev/null; then
    USER_UID=$(id -u)
    USER_GID=$(id -g)

    sudo mkdir -p /data/beta-mamba-pm/{test,prod}/{quetz,postgres,letsencrypt}
    sudo chown -R $USER_UID:$USER_GID /data/beta-mamba-pm
fi