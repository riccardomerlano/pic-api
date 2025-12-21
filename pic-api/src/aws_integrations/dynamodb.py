import boto3
import logging
from utils.env_loader import envs_dict
from utils.env_loader import localstack

logger = logging.getLogger('PIC-API')

dynamo_regions_list = [k for k in envs_dict if 'DYNAMO_REGION' in k]

# Returns a DynamoDB resource for a specific region with difference between localstack and AWS
def instanciate_dynamodb_client(region):
    if localstack:
        logger.info(f"Instanciating localstack DynamoDB client for region: {envs_dict[region]}")
        return boto3.resource(
            "dynamodb",
            region_name=envs_dict[region],
            endpoint_url=envs_dict["LOCALSTACK_HOST"]
        )
    else:
        logger.info(f"Instanciating DynamoDB client for region: {envs_dict[region]}")
        return boto3.resource(
            'dynamodb',
            aws_access_key_id=envs_dict["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=envs_dict["AWS_SECRET_ACCESS_KEY"],
            region_name=envs_dict[region]
        )

# Returns ok/ko for a given table status
def check_client_stauts(table):
    logger.info("Checking DynamoDB region status")
    try:
        table.table_size_bytes
        return "ok"
    except Exception as e:
        return "ko"

# Returns a list of clients for a given list of regions
def get_dynamodb_clients(regions_list):
    logger.info("Getting DynamoDB clients")
    client_list = []
    for region in regions_list:
        client_list.append(instanciate_dynamodb_client(region))
    logger.info("Instanciated DynamoDB clients")
    return client_list

# Returns a working DynamoDB table object relative a DynamoDB list of resources (one for each region)
# If the DynamoDB list of resources does not exists, then this procedure will instanciate them
def get_dynamodb_table():
    logger.info("Instanciating DynamoDB table")
    if not hasattr(get_dynamodb_clients, "_dynamodb_clients"):
        get_dynamodb_clients._dynamodb_clients = get_dynamodb_clients(dynamo_regions_list)
    dynamodb_clients = get_dynamodb_clients._dynamodb_clients
    for client in dynamodb_clients:
        logger.info("Checking for a working DynamoDB region")
        table = client.Table(envs_dict["DYNAMODB_TABLE"])
        client_status = check_client_stauts(table)
        if client_status == "ok":
            logger.info("Found a working DynamoDB region")
            return table
    logger.error("No working region for DynamoDB")
    raise Exception("No working region for DynamoDB")
