output "logging_reader_sa_email" {
  value       = google_service_account.logging_reader.email
  description = "Email of the read-only logging service account."
}

output "logging_reader_sa_name" {
  value       = google_service_account.logging_reader.name
  description = "Resource name of the read-only logging service account."
}

output "logging_viewer_binding" {
  value       = google_project_iam_member.logging_viewer.id
  description = "IAM binding granting roles/logging.viewer."
}