variable "project_id" {
  type = string
  description = "The ID of the Google Cloud project."
}
variable "workload_identity_pool_id" {
  type = string
  description = "The Workload Identity Pool or other user identity to allow impersonation of the service account. Empty if not using Workload Identity."
  default = ""
}
