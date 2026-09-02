resource "google_service_account" "engine" {
  account_id   = "reasoning-engine"
  display_name = "Vertex AI Reasoning Engine"
  project      = var.project
}

resource "google_project_iam_member" "engine" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.objectViewer",
    "roles/secretmanager.secretAccessor",
  ])

  project = var.project
  role    = each.value
  member  = google_service_account.engine.member
}
