#!/bin/bash

# Check if .env file exists
if [ -f .env ]; then
    # Read .env file line by line
    while IFS='=' read -r name value; do
        # Skip empty lines and lines starting with '#'
        if [[ -n $name && ! $name =~ ^# ]]; then
            # Export variable
            export "$name"="$value"
        fi
    done < .env
    echo "Environment variables loaded from .env file"
else
    echo "Error: .env file not found"
fi