import json
from database.db_initialization import run_all_initialization

# pending to refactor into alembiccc


def lambda_handler(event, context):

    print("about to run initialization")
    run_all_initialization()
    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}


# include the execution of lambda handler with empty event and context if this file is just called:
if __name__ == "__main__":
    lambda_handler({}, {})
