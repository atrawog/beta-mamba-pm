#!/usr/bin/env python

import requests
from s3_utils import is_file_size_zero, file_exists_in_s3, remove_file
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("QUETZ_API_KEY")


def get_packages(host, channel):
    url = f"https://{host}/api/channels/{channel}/packages"
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch packages: {response.text}"

def get_package_versions(host, channel, package_name):
    url = f"https://{host}/api/channels/{channel}/packages/{package_name}/versions"
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch versions for package {package_name}: {response.text}"

def fetch_all_versions(host, channel, bucket_name):
    packages = get_packages(host, channel)
    if isinstance(packages, str):
        print(packages)
        return
    sorted_packages = sorted(packages, key=lambda x: x['name'])
    for package in sorted_packages:
        package_name = package['name']
        versions = get_package_versions(host, channel, package_name)
        if isinstance(versions, str):
            print(versions)
            continue
        for version in versions:
            plattform = version['platform']
            filename=version['filename']
            path = f"{version['platform']}/{version['filename']}"
            full_path = f"{bucket_name}:{path}"

            if file_exists_in_s3(bucket_name, path):
                if is_file_size_zero(bucket_name, path):
                    print(f"\nZERO: {full_path}")
                    delete_package_versions(host, channel, package_name,plattform,filename)
                    # remove_file(bucket_name, path)
                else:
                    print(f"OKAY: {full_path}")
            else:
                print(f"\nFAIL: {host} {channel} {package_name} {plattform} {filename}")
                delete_package_versions(host, channel, package_name,plattform,filename)

def delete_package_versions(host, channel, package_name,plattform,filename):
    url = f"https://{host}/api/channels/{channel}/packages/{package_name}/versions/{plattform}/{filename}"
    headers = {
    'X-API-KEY': api_key,
    'accept': 'application/json'
    }
    print(f"DELETE {url}")
    response = requests.delete(url, headers=headers)
    print(f"{response}\n")

# Main script execution
if __name__ == "__main__":
    host = 'quant-prod-quetz-5.mamba.pm'
    channel = 'emscripten-forge'
    bucket_name = 'quetz-gra-emscripten-forge'
    fetch_all_versions(host, channel, bucket_name)
