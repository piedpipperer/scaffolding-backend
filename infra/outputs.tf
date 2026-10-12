# outputs.tf - Cloudflare Deployment Outputs

output "worker_name" {
  description = "The name of the deployed Cloudflare Worker script."
  value       = cloudflare_worker_script.main.name
}

output "custom_domain_route" {
  description = "The configured custom domain route pattern, if defined."
  value       = length(cloudflare_worker_route.custom_route) > 0 ? cloudflare_worker_route.custom_route[0].pattern : "none (using default *.workers.dev subdomain)"
}
