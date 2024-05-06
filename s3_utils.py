import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from dotenv import load_dotenv
import os
import logging

# Load environment variables from a .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def file_exists_in_s3(bucket_name, file_key):
    """
    Check if a file exists in an S3 bucket using credentials from environment variables.
    """
    # Get AWS credentials and configuration from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Default region if not provided
    aws_endpoint_url = os.getenv('AWS_ENDPOINT_URL')  # Custom endpoint URL, if provided

    # Initialize an S3 client using the credentials and configuration
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    s3 = session.client('s3', endpoint_url=aws_endpoint_url)

    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def is_file_size_zero(bucket_name, file_key):
    """
    Check if a file in an S3 bucket has a file size of zero.
    """
    # Get AWS credentials and configuration from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Default region if not provided
    aws_endpoint_url = os.getenv('AWS_ENDPOINT_URL')  # Custom endpoint URL, if provided

    # Initialize an S3 client using the credentials and configuration
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    s3 = session.client('s3', endpoint_url=aws_endpoint_url)

    try:
        response = s3.head_object(Bucket=bucket_name, Key=file_key)
        return response['ContentLength'] == 0
    except ClientError as e:
        logger.error(f"Failed to retrieve object: {e}")
        if e.response['Error']['Code'] == '404':
            return False  # Treat file not found as not zero size
        else:
            raise

def remove_file(bucket_name, file_key):
    """
    Remove a file from an S3 bucket.
    """
    # Get AWS credentials and configuration from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')  # Default region if not provided
    aws_endpoint_url = os.getenv('AWS_ENDPOINT_URL')  # Custom endpoint URL, if provided

    # Initialize an S3 client using the credentials and configuration
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    s3 = session.client('s3', endpoint_url=aws_endpoint_url)

    try:
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        logger.info(f"Deleted file: {file_key}")
    except ClientError as e:
        logger.error(f"Failed to delete object {file_key}: {e}")
        raise
