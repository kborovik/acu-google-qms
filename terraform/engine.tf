resource "google_vertex_ai_reasoning_engine" "engine" {
  provider     = google-beta
  display_name = "Vertex AI Reasoning Engine"
  region       = var.region
  project      = var.project

  spec {
    service_account = google_service_account.engine.email
  }

  context_spec {
    memory_bank_config {}
  }

  depends_on = [google_project_service.apis]
}
