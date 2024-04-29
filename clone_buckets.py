#!/usr/bin/env python 

import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
endpoint_url = os.getenv('S3_ENDPOINT_URL')
aws_region = os.getenv('AWS_REGION')
source_prefix = os.getenv('SOURCE_PREFIX')
target_prefix = os.getenv('TARGET_PREFIX')

def run_aws_cli_command(command):
    """Executes an AWS CLI command and handles the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing AWS CLI command:", e.stderr)
        return None
    return result.stdout

def list_buckets():
    """Lists all S3 buckets and filters them by source prefix."""
    command = f"aws s3 ls --endpoint-url {endpoint_url} --region {aws_region}"
    print(command)
    output = run_aws_cli_command(command)
    if output:
        buckets = [line.split()[-1] for line in output.strip().split('\n')]
        filtered_buckets = [bucket for bucket in buckets if bucket.startswith(source_prefix)]
        return filtered_buckets
    return []

def create_bucket(bucket_name):
    """Creates a new S3 bucket."""
    command=f"aws s3 mb s3://{bucket_name} --endpoint-url {endpoint_url} --region {aws_region}"
    print(command)
    run_aws_cli_command(command)

def sync_buckets(source, target):
    """Syncs all contents from the source bucket to the target bucket."""
    command=f"aws s3 sync s3://{source} s3://{target} --endpoint-url {endpoint_url} --region {aws_region}"
    print(command)
    run_aws_cli_command(command)

if __name__ == "__main__":
    # Get all buckets that match the source prefix
    buckets_to_clone = list_buckets()

    for bucket in buckets_to_clone:
        new_bucket_name = target_prefix + bucket[len(source_prefix):]
        print(f"\nSyncing {bucket} to {new_bucket_name}")
        create_bucket(new_bucket_name)
        sync_buckets(bucket, new_bucket_name)
