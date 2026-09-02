output "reasoning_engine_name" {
  description = "Reasoning engine resource name"
  value       = google_vertex_ai_reasoning_engine.engine.name
}

output "service_account_email" {
  description = "Engine service account email"
  value       = google_service_account.engine.email
}

output "artifact_bucket" {
  description = "GCS artifact bucket name"
  value       = google_storage_bucket.artifacts.name
}

output "gemini_api_key_secret_id" {
  description = "Secret Manager secret ID for the Gemini API key"
  value       = google_secret_manager_secret.gemini_api_key.secret_id
}
