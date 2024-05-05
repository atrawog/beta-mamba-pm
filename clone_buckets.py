#!/usr/bin/env python

import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve all current environment variables
current_env = os.environ.copy()

# Retrieve environment variables for AWS
source_prefix = os.getenv('SOURCE_PREFIX')
target_prefix = os.getenv('TARGET_PREFIX')
bucket_list = os.getenv('BUCKET_LIST')

def run_command(command):
    """Executes a command and handles the output, using the current environment variables."""
    print(f"Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=current_env)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e.stderr)
        return None
    return result.stdout

def get_cors_headers(bucket_name):
    """Gets all CORS-related headers for a specified bucket using swift stat."""
    command = f"swift stat {bucket_name}"
    result = run_command(command)
    headers = {}
    if result:
        lines = result.split('\n')
        for line in lines:
            if "Meta Access-Control-" in line:
                key_part, value = line.split(':', 1)
                key = 'X-Container-' + key_part.strip().replace(' ', '-')
                headers[key] = value.strip()
    return headers

def set_cors_headers(bucket_name, headers):
    """Sets CORS-related headers on a specified bucket using swift post."""
    header_str = ' '.join([f"--header '{key}: {value}'" for key, value in headers.items()])
    command = f"swift post {bucket_name} {header_str}"
    run_command(command)

def list_buckets():
    """Lists all S3 buckets."""
    command = f"aws s3 ls"
    output = run_command(command)
    if output:
        return [line.split()[-1] for line in output.strip().split('\n')]
    return []

def create_bucket(bucket_name, existing_buckets):
    """Creates a new S3 bucket if it does not already exist."""
    if bucket_name not in existing_buckets:
        command = f"aws s3 mb s3://{bucket_name}"
        run_command(command)
    else:
        print(f"Bucket {bucket_name} already exists. Skipping creation.")

def sync_buckets(source, target):
    """Syncs all contents from the source bucket to the target bucket."""
    command = f"aws s3 sync s3://{source} s3://{target}"
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
        cors_headers = get_cors_headers(bucket)
        if cors_headers:
            set_cors_headers(new_bucket_name, cors_headers)
        sync_buckets(bucket, new_bucket_name)
