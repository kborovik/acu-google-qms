resource "google_storage_bucket" "artifacts" {
  name                        = "${var.project}-agent-artifacts"
  location                    = var.region
  project                     = var.project
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}
