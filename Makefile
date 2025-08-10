
# can only be run if venv is working in local.
package_lambda:
	rm -rf lambda_deploy
	mkdir lambda_deploy
	mkdir lambda_deploy/routes
	poetry export --without-hashes --format=requirements.txt --output requirements_poetry.txt --no-interaction --without dev,debug
	poetry run python -m pip install -r requirements_poetry.txt  -t "./lambda_deploy"
	cp -r tiny_relappmidos.py lambda_deploy/
	cp -r db_initialization.py lambda_deploy/
	cp -r routes lambda_deploy/
	cp -r database lambda_deploy/
	cp -r authentication lambda_deploy/
	cp -r config lambda_deploy/
	cp -r alembic_scripts lambda_deploy/alembic_scripts
	cp -r alembic.ini lambda_deploy/alembic.ini
	cd lambda_deploy && zip -r ./deployment_package.zip .
	pwd


# in case of having an html to teste also the backend.
launch_http:
	cd ./static && python -m http.server 8001 && cd ..
