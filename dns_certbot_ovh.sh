certbot certonly --force-renewal  \
    --dns-ovh --non-interactive --agree-tos \
    -m atrawog@gmail.com --dns-ovh-credentials .secrets/certbot_ovh.ini \
    --logs-dir . --dns-ovh-propagation-seconds 60 \
--cert-name beta.mamba.pm \
-d beta.mamba.pm  \
-d repo.mamba.pm  \
-d quant-prod-quetz-4.mamba.pm \
-d quant-prod-quetz-4-repo.mamba.pm \
--work-dir ./data/prod/letsencrypt --config-dir ./data/prod/letsencrypt --logs-dir .