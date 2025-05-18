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
  curl -X 'GET' \
    'http://127.0.0.1:8000/user/users' \
    -H 'accept: text/html' \
    -u "jordi:random_pass"
  ```poetry run python ./database/db_initialization.py

---

## Deployment to AWS Lambda

1. **Package the application for Lambda**
  Run the following command to create a deployment package:
  ```bash
  make package_lambda
  ```


Feel free to add more details about the project in the sections above.

2. add the lambda zip to a lambda function already configured (infra to be seen in the future)

3. configure aws-api-gateway to have this endpoint (or endpoints) that we uploaded configured.

4. an rds posgres (idealy serverless) database must also be cofnigured somewhere on the internet so that the api comunicated with it 
(same vpc)

5. 

