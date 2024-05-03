#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found!"
    exit 1
fi

if sudo -l &>/dev/null; then
    USER_UID=$(id -u)
    USER_GID=$(id -g)

    sudo mkdir -p /data/beta-mamba-pm/{test,prod}/{quetz,postgres,letsencrypt}
    sudo chown -R $USER_UID:$USER_GID /data/beta-mamba-pm
fi


# Create the output directory if it doesn't exist
mkdir -p /data/beta-mamba-pm/prod/quetz/channels

# Write configuration to config.toml
cat > /data/beta-mamba-pm/prod/quetz/config.toml <<EOF
[general]
package_unpack_threads="64"

[github]
# Register the app here: https://github.com/settings/applications/new
# the callback url should be <URL>/auth/github/authorize
client_id = "$CLIENT_ID"
client_secret = "$CLIENT_SECRET"

[sqlalchemy]
database_url = "$DATABASE_URL"

[session]
secret = "$SESSION_SECRET"
https_only = "True"

[s3]
access_key = "$S3_ACCESS_KEY"
secret_key = "$S3_SECRET_KEY"
url = "$S3_URL"
region = "GRA"
#bucket_name=""
bucket_prefix="quetz-prod4-"
bucket_suffix=""

[users]
admins = ['github:atrawog', 'github:wolfv']

[logging]
level = "INFO"
file = "quetz-prod4.log"
EOF

echo "Configuration has been written to /data/beta-mamba-pm/prod/quetz/config.toml"

mkdir -p /data/beta-mamba-pm/test/quetz/channels

# Write configuration to config.toml
cat > /data/beta-mamba-pm/test/quetz/config.toml <<EOF
[github]
# Register the app here: https://github.com/settings/applications/new
client_id = ""
client_secret = ""

[sqlalchemy]
database_url = "postgresql://postgres:postgres@db:5432/quetz"

[session]
secret = "$SESSION_SECRET_TEST"
https_only = true
EOF

echo "Configuration has been written to /data/beta-mamba-pm/test/quetz/config.toml"