-include .env
-include dev.env

.PHONY: run_local deploy dev_cf set_secret_db db_upgrade db_init infra_init infra_plan infra_apply launch_static

# Run local FastAPI server with auto-reload
run_local:
	poetry run uvicorn main:app --reload --port 8000

# Deploy the FastAPI application directly to Cloudflare Workers
deploy:
	npx wrangler deploy

# Run the Cloudflare Worker emulator locally
dev_cf:
	npx wrangler dev

# Set the Neon / PostgreSQL database URL secret in Cloudflare
set_secret_db:
	npx wrangler secret put DATABASE_URL

# Run Alembic migrations against the configured database (e.g. Neon)
db_upgrade:
	poetry run alembic upgrade head

# Run db_initialization script
db_init:
	poetry run python db_initialization.py

# Terraform commands for Cloudflare infrastructure
infra_init:
	cd infra && terraform init

infra_plan:
	cd infra && terraform plan

infra_apply:
	cd infra && terraform apply

# Launch local static file server for testing UI
launch_static:
	cd ./static && python -m http.server 8001
