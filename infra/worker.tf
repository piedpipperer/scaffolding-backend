# worker.tf - Cloudflare Worker Script & Route Definitions

resource "cloudflare_worker_script" "main" {
  account_id          = var.cloudflare_account_id
  name                = "${var.app_name}-${var.environment}"
  content             = file("${path.module}/../main.py")
  compatibility_date  = "2026-09-08"
  compatibility_flags = ["python_workers"]

  plain_text_binding {
    name = "APP_NAME"
    text = var.app_name
  }

  plain_text_binding {
    name = "ENVIRONMENT"
    text = var.environment
  }
}

resource "cloudflare_worker_route" "custom_route" {
  count       = var.cloudflare_zone_id != null && var.custom_domain != null ? 1 : 0
  zone_id     = var.cloudflare_zone_id
  pattern     = var.custom_domain
  script_name = cloudflare_worker_script.main.name
}
