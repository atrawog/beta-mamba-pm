#!/usr/bin/env python 
import ovh
from dotenv import load_dotenv
import os
from dns_utils import delete_records, add_record  # Import the functions from the module

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials and domain settings from environment variables
application_key = os.getenv("APPLICATION_KEY")
application_secret = os.getenv("APPLICATION_SECRET")
consumer_key = os.getenv("CONSUMER_KEY")
domain = os.getenv("DOMAIN")
# Initialize OVH client with credentials
client = ovh.Client(
    endpoint="ovh-eu",
    application_key=application_key,
    application_secret=application_secret,
    consumer_key=consumer_key,
)

add_record(client, domain, 'quant-prod-quetz-4.mamba.pm.', 'A',  '162.19.52.159')

# add_record(client, domain, beta_host, 'CNAME', target)

# Delete and add records for beta and repo subdomains
# delete_records(client, domain, beta_host, 'A')
# delete_records(client, domain, beta_host, 'CNAME')
# add_record(client, domain, beta_host, 'CNAME', target)
# add_record(client, domain, beta_host, 'CNAME', target)

# delete_records(client, domain, repo_host, 'A')
# delete_records(client, domain, repo_host, 'CNAME')
# add_record(client, domain, repo_host, 'CNAME', target)
# add_record(client, domain, repo_host, 'CNAME', target)

# Refresh the domain's DNS zone
endpoint = f'/domain/zone/{domain}/refresh'
client.post(endpoint)
