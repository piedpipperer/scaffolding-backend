import json
import os


import boto3
from botocore.exceptions import ClientError
from functools import lru_cache


@lru_cache()
def is_running_in_lambda():
    # AWS Lambda sets the `AWS_LAMBDA_FUNCTION_NAME` environment variable
    return "AWS_LAMBDA_FUNCTION_NAME" in os.environ


@lru_cache()
def get_db_secret():
    secret_name = "rds!cluster-f394bd70-e9dc-45ff-a012-d095d6ae2a9e"
    # arn: arn:aws:secretsmanager:eu-west-1:617961504899:secret:rds!cluster-f394bd70-e9dc-45ff-a012-d095d6ae2a9e-k9cUaQ
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    if not is_running_in_lambda():
        session = boto3.session.Session(profile_name="jrojo")
    else:
        session = boto3.session.Session()

    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        print("got secret:", secret_name)

    except ClientError as e:
        print("got an error getting the secret:")
        print(e)
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Parse the secret string as JSON
    secret = json.loads(get_secret_value_response["SecretString"])

    return secret


HEADERS = {
    "Access-Control-Allow-Origin": "to_place_frontend_origin",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "authorization, Content-Type, X-Requested-With",
    # "Access-Control-Max-Age": "3600",  # Cache preflight response for 1 hour
}
