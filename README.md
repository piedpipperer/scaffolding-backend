# Relapmidos Backend

This repository contains the backend for general backend to be developed in fastapi, with idea of deploying it in a cloud (aws) in a serverless manner.
Below are the steps to set up and test the application locally, as well as instructions for deployment.

---

## Local Setup and Testing

0. **Set up the Python environment**
  Use Python 3.11 and install dependencies:
  ```bash
  poetry env use python3.11
  source ..
  poetry install
  ```

---

1. **Ensure the database is created**
  Make sure the database specified in the DB connection settings is created and accessible.

2. **Run posgres db localy*
  do the necesary steps to have posgres database localy with a user with permisisons to create db and tables.
  create a database also for the connection (url in the database file config)
  ```
3. **Initialize the database**
  Run the following command to initialize the database:
  ```bash
  poetry run python ./database/db_initialization.py
  ```

4. **Start the FastAPI server**
  Use the following command to start the development server:
  ```bash
  uvicorn tiny_relappmidos:app --reload
  ```
  > **Note:** `tiny_relappmidos` is the name of the file containing the FastAPI app.

5. **Run the fastapi app in local:**
  uvicorn tiny_relappmidos:app --reload

6. **Test the API endpoint**
  You can test the API using `curl`:
  ```bash
  curl -I -X 'GET' \
    'http://127.0.0.1:8000/user/users' \
    -H 'accept: text/html' \
    -u "jordi:1234321"
  ```

# this should return the data.
  ```bash
  curl -X 'GET' \
    'http://127.0.0.1:8000/user/users' \
    -H 'accept: text/html' \
    -u "jordi:1234321"
  ```
7. **test options endpoint**
  ```bash
 curl -i -X OPTIONS "http://127.0.0.1:8000/user/users"      -H "Origin: http://localhost:8000"      -H "Access-Control-Request-Method: GET"      -H "Access-Control-Request-Headers: Authorization, Content-Type"
 -H 'accept: text/html'
  ```
---

## Deployment to AWS Lambda

1. **Package the application for Lambda**
  Run the following command to create a deployment package:
  ```bash
  make package_lambda
  ```


Feel free to add more details about the project in the sections above.

2. add the lambda zip to a lambda function already configured (infra to be seen in the future)
    2.1 will need to asigne thie (general) role i am using (persones) for any lambda to access all services neeeded (and permissions).
    2.2 seems like in the config there is the rds-databases, before that need to configure vpc, subnets and sec. groups. i am including always the same ones.
    in addition then, rds: Have to include the endpoint there.

3. configure aws-api-gateway (redoing this to have it automaticaly created based on openapi)
       - to have this endpoint (or endpoints) that we uploaded configured.

4. an rds posgres (idealy serverless) database must also be cofnigured somewhere on the internet so that the api comunicated with it
(same vpc).
   4.1 go to the query editor and create the database: CREATE DATABASE my_database;

5.

# regarding permissions in aws:

# to check current lambda permsissions:
aws lambda get-function-configuration \
  --function-name relappmidos-initialize_db \
  --profile jrojo \
  --query 'VpcConfig'



# to execute 1nce per lambda.
aws lambda add-permission \
 --statement-id hola_hola_caracola \
 --action lambda:InvokeFunction \
 --function-name "arn:aws:lambda:eu-west-1:617961504899:function:db_initz_relappmidos_app" \
 --principal apigateway.amazonaws.com \
 --source-arn "arn:aws:execute-api:eu-west-1:617961504899:t7hkfitez7/*/*/*/*" \
 --profile jrojo


aws lambda add-permission \
 --statement-id hola_hola_caracola \
 --action lambda:InvokeFunction \
 --function-name "arn:aws:lambda:eu-west-1:617961504899:function:relappmidos" \
 --principal apigateway.amazonaws.com \
 --source-arn "arn:aws:execute-api:eu-west-1:617961504899:t7hkfitez7/*/*/*/*" \
 --profile jrojo



policy for lambda to interact with database:
aws iam create-policy \
    --policy-name LambdaRDSAccessPolicy \
    --policy-document file://aws/lambda-rds-policy.json \
    --profile jrojo

# get role-policy:
aws lambda get-function \
    --function-name tmp_dedicacio-initialize_db \
    --query "Configuration.Role" \
    --profile jrojo

# not needed if already have an api going on.
# attach rdsaccess policy to the lambda role.
aws iam attach-role-policy \
    --role-name persones_endpoint-role-ev4upc5k \
    --policy-arn arn:aws:iam::617961504899:policy/LambdaRDSAccessPolicy \
    --profile jrojo


# not needed if already have an api going on.
aws iam list-attached-role-policies \
    --role-name persones_endpoint-role-ev4upc5k \
    --profile jrojo


# not needed if already have an api going on.
# let's now validate vpc:
aws lambda get-function-configuration \
    --function-name relappmidos \
    --query 'VpcConfig' \
    --profile jrojo

# the previous lambda i created:
aws lambda get-function-configuration \
    --function-name tmp-dedicacio-get_personas \
    --query 'VpcConfig' \
    --profile jrojo

# sth going on with sg permissions:
aws ec2 describe-security-groups \
  --group-ids 'sg-17995864' \
  --query 'SecurityGroups[*].IpPermissions' \
  --profile jrojo

aws ec2 describe-security-groups \
  --group-ids 'sg-0902298280dabb189' \
  --query 'SecurityGroups[*].IpPermissions' \
  --profile jrojo

# reachability analysis.
aws ec2 create-network-insights-path \
  --source relappmidos \
  --destination <RDS_ENI_ID> \
  --protocol TCP \
  --destination-port 5432 \
  --profile jrojo

# FOR THAT, WE NEED THE ENIS:
aws ec2 describe-network-interfaces \
  --filters Name=description,Values="AWS Lambda VPC ENI*" \
            Name=group-id,Values=sg-17995864 \
  --query 'NetworkInterfaces[*].{ID:NetworkInterfaceId, Subnet:SubnetId, PrivateIp:PrivateIpAddress}' \
  --profile jrojo


# sg permissions
aws ec2 describe-security-groups \
  --group-ids sg-17995864 \
  --profile jrojo \
  --query 'SecurityGroups[*].IpPermissions'


aws rds describe-db-instances \
  --db-instance-identifier database-1-instance-1 \
  --query 'DBInstances[*].{Endpoint:Endpoint.Address, SubnetGroup:DBSubnetGroup.Subnets[*].SubnetIdentifier, SGs:VpcSecurityGroups[*].VpcSecurityGroupId}' \
  --profile jrojo

aws ec2 describe-security-groups \
  --group-ids <your-lambda-sg> <your-rds-sg> \
  --profile jrojo

#  once api deployed and working:

7. **test options endpoint**
  ```bash
 curl -i -X OPTIONS "https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod/user/users" -H "Origin: http://localhost:8000" -H "Access-Control-Request-Method: GET"  -H "Access-Control-Request-Headers: Authorization, Content-Type" -H 'accept: text/html'
  ```

(this is for when user is created)
8. **test only get enpoint**  (working)
  ```bash
  curl -X GET "https://d63ojp7jad.execute-api.eu-west-1.amazonaws.com/prod/user/users"  \
  -u "jordi:1234321" \
  -H "Origin: http://localhost:8000"  \
  -H "Content-Type: application/json"
  ```