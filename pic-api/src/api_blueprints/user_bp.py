import re
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import logging
from aws_integrations.s3 import get_working_s3_client, get_s3_info
from aws_integrations.dynamodb import get_dynamodb_table
from utils.env_loader import envs_dict

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

logger = logging.getLogger('PIC-API')

user_routes = Blueprint("user_routes", __name__)

# /users route:
# method GET: return 200 with list of users in json format or 500 if DynamoDB is not working
@user_routes.route("/users", methods=["GET"])
def users():
    try:
        dynamodb_table = get_dynamodb_table()
        response = dynamodb_table.scan()
        return jsonify(response.get("Items", [])), 200
    except Exception as e:
        logger.error(f"Error for DynamoDB in calling /users endpoint: {str(e)}")
        return  jsonify({"error": f"Internal DynamoDB error: {str(e)}"}), 500

# /users route:
# method GET: 
# - 200 with single user detail in json format
# - 404 if user name passed as url parameter is not found
# - 400 if missing user name in url parameter
# - 500 if DynamoDB is not working
# method POST: 
# - 200 if user added both in dynamo and s3
# - 400 if user name is unspecified, contains unallowed characters or already present on DynamoDB
# - 500 if either DynamoDB or S3 is not working
@user_routes.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        s3_client = get_working_s3_client()
        s3_bucket, s3_region = get_s3_info()
        user_data = request.form.to_dict()

        if user_data["name"] is None:
            return jsonify({"error": "name field must be specified"}), 400
        else:
            if re.search("^[a-zA-Z0-9_.-]*$", user_data["name"]) is None:
                return jsonify({"error": "name field must can contain just letters, numbers, _ and -"}), 400
            else:
                try:
                    logger.info(f"Searching if user {user_data['name']} already present in DynamoDB table")
                    dynamodb_table = get_dynamodb_table()
                    response = dynamodb_table.get_item(Key={"name": user_data["name"]})
                    user_info = response["Item"]
                except KeyError:
                    logger.info(f"User {user_data['name']} not present in DynamoDB table")
                else:
                    return jsonify({"error": "user name already present, please chose another name"}), 400

        if request.files.get('avatar') is not None and request.files.get('avatar').filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            avatar = request.files.get('avatar')
            filename = f"{user_data['name']}/{secure_filename(avatar.filename)}" 
        else:
            logger.info("Missing or not allowed avatar in calling /user: fallback to default image")
            avatar = None
            filename = envs_dict["DEFAULT_IMAGE_SUBPATH"]
            
        s3_path = f"https://{s3_bucket}.s3.{s3_region}.amazonaws.com/{filename}"

        try:
            logger.info("Updating DynamoDB with user data")
            user_data['avatar_url'] = s3_path
            dynamodb_table = get_dynamodb_table()
            dynamodb_table.put_item(Item=user_data)
        except Exception as e:
            return  jsonify({"error": f"Internal DynamoDB error: {str(e)}"}), 500
        
        if avatar is not None:
            try:
                logger.info("Updating S3 with user data in calling /user endpoint")
                s3_client = get_working_s3_client()
                s3_client.upload_fileobj(
                    avatar, s3_bucket, filename
                )
            except Exception as e:
                return  jsonify({"error": f"Internal S3 error: {str(e)}"}), 500 

        return jsonify({"s3_path": f"{s3_path}", "dynamodb": "updated"}), 200
    else:
        user_name = request.args.get('name') 
        if not user_name:
            return jsonify({"error": "Missing required parameter: name"}), 400
        
        try:
            logger.info(f"Retrieving data from DynamoDB in /user calling for user: {user_name}")
            dynamodb_table = get_dynamodb_table()
            response = dynamodb_table.get_item(Key={"name": user_name}) 
            return jsonify(response["Item"]), 200
        except KeyError:
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return  jsonify({"error": f"Internal DynamoDB error: {str(e)}"}), 500

