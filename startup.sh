#!/bin/bash

# Retrieve the user's UID and GID once at the start
USER_UID=$(id -u)
USER_GID=$(id -g)

export USER_UID USER_GID  # Export the UID and GID to make them available in subshells

# Function to change ownership of a file or directory if it exists and if needed
change_ownership_if_needed() {
    local path="$1"
    if [[ -e "$path" ]]; then  # Check if the file or directory exists
        # Retrieve the user ID of the path's owner
        local current_uid=$(stat -c "%u" "$path")

        # Only change ownership if the current UID does not match the user's UID
        if [[ $current_uid -ne $USER_UID ]]; then
            echo "Changing ownership of $path"
            if ! sudo chown "$USER_UID:$USER_GID" "$path"; then
                echo "Failed to change ownership of $path" >&2
                return 1
            fi
        fi
    else
        echo "$path does not exist"
        return 1
    fi
}

export -f change_ownership_if_needed  # Export the function to make it available in subshells

# Function to recursively process each file/directory within a specified path
process_directory() {
    local dir=$1
    if [[ -d "$dir" ]]; then
        # Find all files and directories and process them in parallel
        find "$dir" -print0 | xargs -0 -n 1 -P 1024 -I {} bash -c 'change_ownership_if_needed "{}"'
    else
        echo "$dir is not a directory"
    fi
}

# Check if sudo privileges are available
if sudo -l &>/dev/null; then
    # Directories to change ownership
    declare -a directories=("/var/run/docker.sock" "/data")

    # Check and append MAMBA_ROOT_PREFIX if it is set and non-empty
    if [[ -n $MAMBA_ROOT_PREFIX ]]; then
        directories+=("$MAMBA_ROOT_PREFIX")
    else
        echo "MAMBA_ROOT_PREFIX is not set or empty."
    fi

    # Iterate through directories and change ownership only if necessary
    for dir in "${directories[@]}"; do
        process_directory "$dir"
    done
else
    echo "No sudo privileges available."
    exit 1
fi


cd /data && quetz create --create-conf /data/beta
cd /data/beta && quetz start . --port 8000 --host 0.0.0.0 --proxy-headers --reload --log-level=trace