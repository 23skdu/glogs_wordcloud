resource "google_service_account" "logging_reader" {
  account_id   = "logging-reader-sa"  # Replace with your desired service account ID
  display_name = "Logging Reader Service Account"
}

resource "google_project_iam_member" "logging_reader_role" {
  project = var.project_id  # Replace with your Google Cloud Project ID
  role    = "roles/logging.viewer"  # Grants read-only access to logs

  member = "serviceAccount:${google_service_account.logging_reader.email}"
}


# Optional: Allow Workload Identity to impersonate the Service Account
# This is needed if you're running your Terraform/application on a system
# that uses Workload Identity (e.g., GKE, GCE with specific configurations).
# If you're not using Workload Identity, you can skip this section.

resource "google_project_iam_member" "workload_identity_user" {
  project = var.project_id  # Replace with your Google Cloud Project ID
  role    = "roles/iam.serviceAccountTokenCreator"

  member = "serviceAccount:${var.workload_identity_pool_id}" # The user or identity pool allowed to assume
  service_account_id = google_service_account.logging_reader.name
}



output "logging_reader_sa_email" {
  value = google_service_account.logging_reader.email
  description = "The email address of the logging reader service account."
}


output "logging_reader_sa_name" {
  value = google_service_account.logging_reader.name
  description = "The full name of the logging reader service account, used for grants"
}

variable "project_id" {
  type        = string
  description = "The ID of the Google Cloud project."
}

variable "workload_identity_pool_id" {
  type = string
  description = "The Workload Identity Pool or other user identity to allow impersonation of the service account. Empty if not using Workload Identity."
  default = ""
}
