#!/bin/bash

# Check if sudo privileges are available
if sudo -l &>/dev/null; then
    USER_UID=$(id -u)
    USER_GID=$(id -g)

    # Attempt to change ownership of docker.sock and handle possible failure
    if ! sudo chown -R "$USER_UID:$USER_GID" /var/run/docker.sock; then
        echo "Error changing owner of /var/run/docker.sock"
    fi

    # Attempt to change ownership of /data and handle possible failure
    if ! sudo chown -R "$USER_UID:$USER_GID" /data; then
        echo "Error changing owner of /data"
    fi

    # Check database connection with wait-for-it.sh and handle possible failure
    if ! sudo wait-for-it.sh db:5432; then
        echo "Database connection failed"
    fi
else
    echo "Sudo privileges are not available."
fi

# Initialize the database and handle possible failure
if ! quetz init-db /data; then
    echo "Failed to initialize database"
fi

# Start the quetz server and handle possible failure
if ! quetz start /data --port 8000 --host 0.0.0.0 --proxy-headers --reload --log-level=trace; then
    echo "Failed to start quetz server"
fi

# Loop indefinitely
while true; do
    sleep 1  # Sleeps for 1 second to avoid high CPU usage
done
