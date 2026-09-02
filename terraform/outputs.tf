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
