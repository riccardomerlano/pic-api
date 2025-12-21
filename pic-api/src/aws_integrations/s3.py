import boto3
import logging
from utils.env_loader import envs_dict
from utils.env_loader import localstack

logger = logging.getLogger('PIC-API')

s3_regions_dict = {k: v for k, v in envs_dict.items() if 'S3_REGION' in k}

# Getting S3 bucket and reagion name for actual working S3 region
def get_s3_info():
    logger.info(f"Retrieving working S3 client information")
    s3_bucket = envs_dict["S3_BUCKET"]
    return f"{s3_bucket}-{envs_dict['S3_ACTUAL_REGION']}", envs_dict["S3_ACTUAL_REGION"]

# Returns a S3 client for a specific region with difference between localstack and AWS
def instanciate_s3_client(region):
    if localstack:
        logger.info(f"Instanciating localstack S3 client for region: {envs_dict[region]}")
        return boto3.client(
            "s3",
            region_name=envs_dict[region],
            endpoint_url=envs_dict["LOCALSTACK_HOST"]
        )
    else:
        logger.info(f"Instanciating S3 client for region: {envs_dict[region]}")
        return boto3.client(
            's3',
            aws_access_key_id=envs_dict["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=envs_dict["AWS_SECRET_ACCESS_KEY"],
            region_name=envs_dict[region]
        )

# Returns ok/ko for client status check
def check_client_stauts(client):
    logger.info("Checking S3 region status")
    try:
        client.list_buckets()
        return "ok"
    except Exception as e:
        return "ko"

# Returns a dictionary like {region: s3_client} for a list of regions
def get_s3_clients(regions_dict):
    logger.info("Getting S3 clients")
    client_dict = {}
    region_keys = regions_dict.keys()
    for region_key in region_keys:
        client_dict[region_key] = instanciate_s3_client(region_key)
    logger.info("Instanciated S3 clients")
    return client_dict

# Returns a working s3 client taken from a list of clients in the form of dictionary like {region: s3_client}
# If the dictionary did not exists, then instanciate the client and return a working one
def get_working_s3_client():
    logger.info("Instanciating S3 clients")
    # Initialize s3_clients only once and reuse it
    if not hasattr(get_working_s3_client, "_s3_clients"):
        get_working_s3_client._s3_clients = get_s3_clients(s3_regions_dict)
    s3_clients = get_working_s3_client._s3_clients
    regions_keys = s3_clients.keys()
    for region_key in regions_keys:
        logger.info(f"Checking for a working S3 region: trying with {envs_dict[region_key]}")
        client_status = check_client_stauts(s3_clients[region_key])
        if client_status == "ok":
            logger.info(f"Found a working S3 region: {envs_dict[region_key]}")
            envs_dict["S3_ACTUAL_REGION"] = envs_dict[region_key]
            return s3_clients[region_key]
    logger.error("No working region for S3")
    raise Exception("No working region for S3")
