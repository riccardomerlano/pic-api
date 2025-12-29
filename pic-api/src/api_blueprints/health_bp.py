from flask import Blueprint, jsonify
import logging
from aws_integrations.s3 import get_working_s3_client
from aws_integrations.dynamodb import get_dynamodb_table
from utils.env_loader import env_loader

health_routes = Blueprint("health_routes", __name__)

logger = logging.getLogger('PIC-API')

# /health route returns 200 if there is a working DynamoDB table and a working S3 client if localstack is in use
# if localstack isn't in use it returns 200 anyway since this is not a production ready component
# in other cases it will return a 500
@health_routes.route("", methods=["GET"])
def health():
    if env_loader.localstack:
        try:
            table = get_dynamodb_table()
        except Exception as e:
            logger.error(f"Error for DynamoDB in calling /health endpoint: {str(e)}")
            return jsonify({"status": "DynamoDB error"}), 500
        
        try:
            s3_client = get_working_s3_client()
            s3_client.list_buckets()
        except Exception as e:
            logger.error(f"Error for S3 in calling /health endpoint: {str(e)}")
            return jsonify({"status": "S3 error"}), 500
    
    return jsonify({"status": "ok"}), 200