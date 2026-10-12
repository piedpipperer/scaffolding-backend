# Cloudflare Infrastructure & Deployment Guide

This directory manages the infrastructure for deploying the FastAPI application to **Cloudflare Workers** with **Neon Serverless PostgreSQL**.

## Architecture Highlights
- **Compute**: Cloudflare Workers with native Python ASGI runtime.
- **Database**: Neon Serverless PostgreSQL over direct secure TLS connection (`sslmode=require`).
- **Networking**: Zero VPC, NAT Gateway, or Subnet overhead. Cloudflare Workers provides native outbound internet access out of the box (for Telegram Bot API, Google OAuth, external webhooks) and instant global public HTTPS URLs.
- **Client Access**: Ready for Telegram bot webhooks, web frontends, and mobile apps (CORS enabled).

---

## Deployment Option 1: Manual / Fast CLI Deployment with Wrangler (Recommended)

Wrangler is the official Cloudflare CLI and the fastest way to develop and deploy Python Workers.

### 1. Authenticate with Cloudflare
```bash
npx wrangler login
```

### 2. Configure Database Secret
Set your Neon connection string as an encrypted Worker secret:
```bash
make set_secret_db
# Or directly:
npx wrangler secret put DATABASE_URL
# When prompted, paste:
# postgresql://<user>:<password>@<neon-endpoint>.aws.neon.tech/<dbname>?sslmode=require
```

### 3. Deploy the Application
```bash
make deploy
# Or directly:
npx wrangler deploy
```
Wrangler will output the live public URL (e.g. `https://scaffolding-backend.<subdomain>.workers.dev`).

### 4. Run Migrations against Neon
```bash
make db_upgrade
```

---

## Deployment Option 2: Terraform IaC Deployment

If you prefer provisioning Cloudflare resources through Terraform:

### 1. Create a `terraform.tfvars` file
In the `infra/` folder, create `terraform.tfvars`:
```hcl
cloudflare_api_token  = "your-cloudflare-api-token"
cloudflare_account_id = "your-cloudflare-account-id"
app_name              = "scaffolding-backend"
environment           = "prod"

# Optional: Custom domain routing (if your zone is on Cloudflare)
# cloudflare_zone_id = "your-zone-id"
# custom_domain      = "api.yourdomain.com/*"
```

### 2. Plan and Apply
From the root directory:
```bash
make infra_init
make infra_plan
make infra_apply
```

---

## Publishing Endpoints for Telegram Bot & Mobile / Web Apps

### 1. Telegram Bot Webhook
Register your Cloudflare Worker URL with Telegram:
```bash
curl -F "url=https://<your-worker-url>/telegram/webhook" \
  https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook
```

### 2. Web & Mobile Apps
Your worker provides automatic HTTPS with CORS preconfigured in `main.py`:
- Interactive Swagger UI: `https://<your-worker-url>/docs`
- ReDoc UI: `https://<your-worker-url>/redoc`
