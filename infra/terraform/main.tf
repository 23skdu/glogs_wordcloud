resource "google_service_account" "logging_reader" {
  account_id   = var.service_account_id
  display_name = "Logging Reader Service Account (read-only)"
  description  = "Read-only access to Cloud Logging for glogs-wordcloud."

  lifecycle {
    prevent_destroy = false
  }
}

# Least-privilege: read-only access to logs.
resource "google_project_iam_member" "logging_viewer" {
  project = var.project_id
  role    = "roles/logging.viewer"
  member  = "serviceAccount:${google_service_account.logging_reader.email}"
}

# Optional: allow a Workload Identity principal to impersonate the service account.
resource "google_service_account_iam_member" "workload_identity_user" {
  count = var.enable_workload_identity && var.workload_identity_principal != "" ? 1 : 0

  service_account_id = google_service_account.logging_reader.name
  role               = "roles/iam.workloadIdentityUser"
  member             = var.workload_identity_principal
}