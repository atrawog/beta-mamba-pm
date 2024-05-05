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

delete_records(client, domain, 'quant-prod-quetz-4.mamba.pm.', 'A')
add_record(client, domain, 'quant-prod-quetz-4.mamba.pm.', 'A',  '51.178.59.67')
add_record(client, domain, 'quant-prod-quetz-4-repo.mamba.pm.', 'CNAME', 'quant-prod-quetz-4.mamba.pm.')

endpoint = f'/domain/zone/{domain}/refresh'
client.post(endpoint)
