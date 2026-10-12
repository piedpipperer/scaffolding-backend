# variables.tf - Cloudflare & Infrastructure Variables

variable "cloudflare_api_token" {
  description = "The Cloudflare API Token with permissions to manage Workers."
  type        = string
  sensitive   = true
}

variable "cloudflare_account_id" {
  description = "The Cloudflare Account ID."
  type        = string
}

variable "app_name" {
  description = "The name of the application and worker."
  type        = string
  default     = "scaffolding-backend"
}

variable "environment" {
  description = "The target environment (e.g. dev, staging, prod)."
  type        = string
  default     = "prod"
}

variable "cloudflare_zone_id" {
  description = "Optional Cloudflare Zone ID for custom domain routing."
  type        = string
  default     = null
}

variable "custom_domain" {
  description = "Optional custom domain route pattern (e.g. api.example.com/*)."
  type        = string
  default     = null
}
