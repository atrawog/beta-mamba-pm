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
    sudo mkdir -p ./data/{test,prod}/{quetz,postgres,letsencrypt,traefik,nginx}
    sudo chown -R $USER_UID:$USER_GID ./data
    sudo chown -R $USER_UID:$USER_GID ./data/{test,prod}/{quetz,letsencrypt,traefik,nginx}
    sudo chown -R 999:$USER_GID ./data/{test,prod}/postgres

fi

mkdir -p ./data/test/quetz/channels
cat > ./data/test/quetz/config.toml <<EOF
[github]
# Register the app here: https://github.com/settings/applications/new
client_id = ""
client_secret = ""

[sqlalchemy]
database_url = "$DATABASE_URL"

[session]
secret = "$SESSION_SECRET_TEST"
https_only = true
EOF

echo "Configuration has been written to ./data/test/quetz/config.toml"

mkdir -p ./data/prod/quetz/channels
cat > ./data/prod/quetz/config.toml <<EOF
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
access_key = "$AWS_ACCESS_KEY_ID"
secret_key = "$AWS_SECRET_ACCESS_KEY"
url = "$AWS_ENDPOINT_URL"
region = "$AWS_REGION"
bucket_prefix="quetz-prod4-"
bucket_suffix=""

[users]
admins = ['github:atrawog', 'github:wolfv']

[logging]
level = "INFO"
file = "quetz-prod4.log"
EOF

echo "Configuration has been written to ./data/prod/quetz/config.toml"


cat > ./data/prod/nginx/nginx.conf <<'EOF'
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    client_max_body_size 2000M;
    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    gzip on;
    gzip_types
        text/plain
        text/css
        text/js
        text/xml
        text/javascript
        application/x-javascript
        application/javascript
        application/json
        application/xml
        application/rss+xml
        image/svg+xml;
    gzip_proxied no-cache no-store private expired auth;

    include /etc/nginx/conf.d/*.conf;

    # hard copied from nginx-certbot for now
    ssl_session_cache shared:le_nginx_SSL:10m;
    ssl_session_timeout 1440m;
    ssl_session_tickets off;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";

server {
        listen 80;
        listen [::]:80;

        listen 443 ssl;
        server_name quant-prod-quetz-4-repo.mamba.pm  repo.mamba.pm;

        rewrite ^/(.*)$ /get/$1 break;

        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            proxy_pass http://quetz:8000;
        }

        location ~ ^/.+\.(json|html)$ {
            add_header Cache-Control $sent_http_cache_control;
            add_header Content-Size $sent_http_content_size;
            add_header ETag $sent_http_etag;
            add_header Last-Modified $sent_http_last_modified;

            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;
            proxy_pass http://quetz:8000;
        }

        ssl_certificate /etc/letsencrypt/live/beta.mamba.pm/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/beta.mamba.pm/privkey.pem; # managed by Certbot

        # Redirect non-https traffic to https
        if ($scheme != "https") {
            return 301 https://$host$request_uri;
        } # managed by Certbot
    }


    server {
        server_name quant-prod-quetz-4.mamba.pm  beta.mamba.pm;

        listen 80 default_server;
        listen [::]:80 default_server;

        listen 443 ssl; # managed by Certbot

        # location ~ /(api|metrics|metricsp|get|auth|docs|redoc|openapi.json) {
        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;

            proxy_pass http://quetz:8000;
        }

        location @getindex {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
            proxy_buffering off;

            proxy_pass http://quetz:8000;
        }

        # RSA certificate
        ssl_certificate /etc/letsencrypt/live/beta.mamba.pm/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/beta.mamba.pm/privkey.pem; # managed by Certbot

        # Redirect non-https traffic to https
        if ($scheme != "https") {
            return 301 https://$host$request_uri;
        } # managed by Certbot
    }
}

EOF

echo "Configuration has been written to ./data/prod/nginx/nginx.conf"

