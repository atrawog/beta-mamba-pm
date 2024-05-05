#!/usr/bin/env python

import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for AWS
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
endpoint_url = os.getenv('AWS_ENDPOINT_URL')
aws_region = os.getenv('AWS_REGION')
source_prefix = os.getenv('SOURCE_PREFIX')
target_prefix = os.getenv('TARGET_PREFIX')
bucket_list = os.getenv('BUCKET_LIST')

# Retrieve Swift authentication environment variables
os_username = os.getenv('OS_USERNAME')
os_password = os.getenv('OS_PASSWORD')
os_auth_url = os.getenv('OS_AUTH_URL')
os_tenant_name = os.getenv('OS_TENANT_NAME')
os_tenant_id = os.getenv('OS_TENANT_ID')
os_identity_api_version = os.getenv('OS_IDENTITY_API_VERSION', '2')  # Default to API version 2
os_region_name = os.getenv('OS_REGION_NAME')

# Check if required Swift environment variables are present
if not all([os_username, os_password, os_auth_url, os_tenant_name, os_tenant_id, os_region_name]):
    print("Missing one or more OpenStack Swift authentication environment variables.")
    exit(1)

def run_command(command):
    """Executes a command and handles the output."""
    print(f"{command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e.stderr)
        return None
    return result.stdout

def get_cors_configuration(bucket_name):
    """Gets the CORS configuration for a specified bucket using swift stat."""
    command = f"swift -V {os_identity_api_version} --os-username {os_username} --os-password {os_password} --os-auth-url {os_auth_url} --os-tenant-name {os_tenant_name} --os-tenant-id {os_tenant_id} --os-region-name {os_region_name} stat {bucket_name}"
    result = run_command(command)
    if result:
        for line in result.split('\n'):
            if "X-Container-Meta-Access-Control-Allow-Origin" in line:
                print(line)
                return line.split(': ')[1].strip()
    print(f"No CORS configuration found for {bucket_name}")
    return None

def set_cors_configuration(bucket_name, cors_origin):
    """Sets the CORS configuration on a specified bucket using swift post."""
    command = f"swift -V {os_identity_api_version} --os-username {os_username} --os-password {os_password} --os-auth-url {os_auth_url} --os-tenant-name {os_tenant_name} --os-tenant-id {os_tenant_id} --os-region-name {os_region_name} post {bucket_name} --header 'X-Container-Meta-Access-Control-Allow-Origin: {cors_origin}'"
    run_command(command)

def list_buckets():
    """Lists all S3 buckets."""
    command = f"aws s3 ls --endpoint-url {endpoint_url} --region {aws_region}"
    output = run_command(command)
    if output:
        return [line.split()[-1] for line in output.strip().split('\n')]
    return []

def create_bucket(bucket_name, existing_buckets):
    """Creates a new S3 bucket if it does not already exist."""
    command = f"aws s3 mb s3://{bucket_name} --endpoint-url {endpoint_url} --region {aws_region}"
    run_command(command)

def sync_buckets(source, target):
    """Syncs all contents from the source bucket to the target bucket."""
    command = f"aws s3 sync s3://{source} s3://{target} --endpoint-url {endpoint_url} --region {aws_region}"
    run_command(command)

if __name__ == "__main__":
    # List all buckets
    all_buckets = list_buckets()

    # Process bucket list if specified
    if bucket_list:
        bucket_list = bucket_list.split(',')  # Split bucket list into individual names
        buckets_to_clone = [source_prefix + name for name in bucket_list if (source_prefix + name) in all_buckets]
    else:
        # Get all buckets that match the source prefix
        buckets_to_clone = [bucket for bucket in all_buckets if bucket.startswith(source_prefix)]

    for bucket in buckets_to_clone:
        new_bucket_name = target_prefix + bucket[len(source_prefix):]
        print(f"\nSyncing {bucket} to {new_bucket_name}")
        create_bucket(new_bucket_name, all_buckets)
        cors_origin = get_cors_configuration(bucket)
        if cors_origin:
            set_cors_configuration(new_bucket_name, cors_origin)
        sync_buckets(bucket, new_bucket_name)
