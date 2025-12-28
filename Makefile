
include dev.env

# can only be run if venv is working in local.
package_lambda: update_lambda_env
	rm -rf lambda_deploy
	mkdir lambda_deploy
	mkdir lambda_deploy/routes
	poetry export --without-hashes --format=requirements.txt --output requirements_poetry.txt --no-interaction --without dev,debug
	poetry run python -m pip install -r requirements_poetry.txt  -t "./lambda_deploy"
	cp -r main.py lambda_deploy/
	cp -r db_initialization.py lambda_deploy/
	cp -r routes lambda_deploy/
	cp -r use_cases lambda_deploy/
	cp -r database lambda_deploy/
	cp -r authentication lambda_deploy/
	cp -r config lambda_deploy/
	cp -r alembic_scripts lambda_deploy/alembic_scripts
	cp -r alembic.ini lambda_deploy/alembic.ini
	cd lambda_deploy && zip -r ./deployment_package.zip .
	cd lambda_deploy && zip -r ./deployment_package.zip . && cd ..
	find lambda_deploy -mindepth 1 ! -name 'deployment_package.zip' -delete
	aws lambda update-function-code --function-name $(APP_NAME) --zip-file fileb://lambda_deploy/deployment_package.zip --profile jrojo
	# aws lambda update-function-code --function-name $(APP_NAME)-initialize_db --zip-file fileb://lambda_deploy/deployment_package.zip --profile jrojo
	pwd

update_lambda_env:
	# This command is not 100% robust if your env var values contain special characters.
	# For a more robust solution, consider using a Python script with python-dotenv and boto3.
	VARS=$$(cat dev.env | grep -v '^#' | grep -v '^$$' | awk -F'=' '{printf "%s=%s,", $$1, $$2}' | sed 's/,$//')
	aws lambda update-function-configuration --function-name $(APP_NAME) --environment "Variables={$(VARS)}" --profile jrojo

update_all_lambda:
	make package_lambda
	make update_lambda_env

# in case of having an html to teste also the backend.
launch_http:
	cd ./static && python -m http.server 8001 && cd ..


 # python -m http.server 8080


load_env_vars:
	source dev.env
