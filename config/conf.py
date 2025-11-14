import json
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError
from functools import lru_cache


@lru_cache()
def is_running_in_lambda():
    # AWS Lambda sets the `AWS_LAMBDA_FUNCTION_NAME` environment variable
    return "AWS_LAMBDA_FUNCTION_NAME" in os.environ


@lru_cache()
def get_db_secret():
    secret_name = "troubleshoot/rds/credentials"
    # arn: arn:aws:secretsmanager:eu-west-1:617961504899:secret:troubleshoot/rds/credentials-lQ5lkD
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

# Load .env only once (usually from the project root)
if not is_running_in_lambda():
    load_dotenv(dotenv_path="./dev.env")


# Optionally expose environment variables through a helper
def get_env_var(key: str, default=None):
    """Get an environment variable with an optional default."""
    return os.getenv(key, default)
