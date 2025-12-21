# test_app.py
import pytest
from src.main import app
from src.utils.env_loader import envs_dict
from moto import mock_aws
import boto3

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@mock_aws
def test_user_post_200(client):
    s3 = boto3.client('s3', region_name=envs_dict["S3_REGION_1"])
    s3.create_bucket(Bucket=f"{envs_dict['S3_BUCKET']}-{envs_dict['S3_REGION_1']}", CreateBucketConfiguration={'LocationConstraint': envs_dict['S3_REGION_1']})
    dynamodb = boto3.client('dynamodb', region_name=envs_dict['DYNAMO_REGION_1'])
    dynamodb.create_table(
        TableName=envs_dict['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'name', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    with open('tests/resources/user-avatar.png', 'rb') as img_file:
        data = {
            'name': "test-user",
            "email": "test@email.com",
            'avatar': (img_file, 'test.png')
        }
        response = client.post('/api/v1/user', data=data, content_type='multipart/form-data')

    assert response.status_code == 200
    assert 'dynamodb' in response.get_json()
    assert 's3_path' in response.get_json()

@mock_aws
def test_user_post_400(client):
    s3 = boto3.client('s3', region_name=envs_dict["S3_REGION_1"])
    s3.create_bucket(Bucket=f"{envs_dict['S3_BUCKET']}-{envs_dict['S3_REGION_1']}", CreateBucketConfiguration={'LocationConstraint': envs_dict['S3_REGION_1']})
    dynamodb = boto3.client('dynamodb', region_name=envs_dict['DYNAMO_REGION_1'])
    dynamodb.create_table(
        TableName=envs_dict['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'name', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    with open('tests/resources/user-avatar.png', 'rb') as img_file:
        data = {
            'name': "test user",
            "email": "test@email.com",
            'avatar': (img_file, 'test.png')
        }
        response = client.post('/api/v1/user', data=data, content_type='multipart/form-data')

    assert response.status_code == 400
    assert response.get_json() == {'error': 'name field must can contain just letters, numbers, _ and -'}

@mock_aws
def test_user_post_500(client):

    with open('tests/resources/user-avatar.png', 'rb') as img_file:
        data = {
            'name': "test-user",
            "email": "test@email.com",
            'avatar': (img_file, 'test.png')
        }
        response = client.post('/api/v1/user', data=data, content_type='multipart/form-data')

    assert response.status_code == 500

@mock_aws
def test_user_get_200(client):
    dynamodb = boto3.client('dynamodb', region_name=envs_dict['DYNAMO_REGION_1'])
    dynamodb.create_table(
        TableName=envs_dict['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'name', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    response = dynamodb.put_item(
        TableName=envs_dict['DYNAMODB_TABLE'], Item={'name':{'S':'test-user'},'email':{'S':'test@email.com'},'avatar_url':{'S':f"https://{envs_dict['S3_BUCKET']}-{envs_dict['S3_REGION_1']}.s3.{envs_dict['S3_REGION_1']}.amazonaws.com/test-user/a1.jpg"}}
    )

    response = client.get('/api/v1/user?name=test-user')

    assert response.status_code == 200
    assert response.get_json() == {
        'name': 'test-user',
        'email': 'test@email.com',
        'avatar_url': f'https://{envs_dict["S3_BUCKET"]}-{envs_dict["S3_REGION_1"]}.s3.{envs_dict["S3_REGION_1"]}.amazonaws.com/test-user/a1.jpg'
    }

@mock_aws
def test_user_get_500(client):

    response = client.get('/api/v1/user?name=test-user')

    assert response.status_code == 500

@mock_aws
def test_user_get_404(client):
    dynamodb = boto3.client('dynamodb', region_name=envs_dict['DYNAMO_REGION_1'])
    dynamodb.create_table(
        TableName=envs_dict['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'name', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    response = client.get('/api/v1/user?name=test-user')

    assert response.status_code == 404
    assert response.get_json() == {'error': 'User not found'}

@mock_aws
def test_users_200(client):
    dynamodb = boto3.client('dynamodb', region_name=envs_dict['DYNAMO_REGION_1'])
    dynamodb.create_table(
        TableName=envs_dict['DYNAMODB_TABLE'],
        KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'name', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    response = dynamodb.put_item(
        TableName=envs_dict['DYNAMODB_TABLE'], Item={'name':{'S':'test-user'},'email':{'S':'test@email.com'},'avatar_url':{'S':f"https://{envs_dict['S3_BUCKET']}-{envs_dict['S3_REGION_1']}.s3.{envs_dict['S3_REGION_1']}.amazonaws.com/test-user/a1.jpg"}}
    )

    response = client.get('/api/v1/users')

    assert response.status_code == 200
    assert response.get_json() == [{
        'name': 'test-user',
        'email': 'test@email.com',
        'avatar_url': f'https://{envs_dict["S3_BUCKET"]}-{envs_dict["S3_REGION_1"]}.s3.{envs_dict["S3_REGION_1"]}.amazonaws.com/test-user/a1.jpg'
    }]
    
@mock_aws
def test_404(client):
    response = client.get('/api/v1/something')

    assert response.status_code == 404