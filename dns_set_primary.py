#!/usr/bin/env python 
import ovh
from dotenv import load_dotenv
import os
from dns_utils import delete_records, add_record, refresh  # Import the functions from the module

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

delete_records(client, domain, 'beta.mamba.pm.', 'CNAME')
delete_records(client, domain, 'repo.mamba.pm.', 'CNAME')
add_record(client, domain, 'beta.mamba.pm.', 'CNAME', 'quant-prod-quetz-4.mamba.pm.')
add_record(client, domain, 'repo.mamba.pm.', 'CNAME', 'quant-prod-quetz-4.mamba.pm.')
refresh(client, domain)

endpoint=f'/domain/zone/{domain}/export'
zone_export = client.get( endpoint)
print (zone_export)