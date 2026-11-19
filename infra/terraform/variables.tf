variable "project_id" {
  type        = string
  description = "The ID of the Google Cloud project."

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "project_id must be a valid Google Cloud project ID."
  }
}

variable "region" {
  type        = string
  description = "Default region for Google Cloud resources."
  default     = "us-central1"
}

variable "service_account_id" {
  type        = string
  description = "ID of the read-only logging service account."
  default     = "logging-reader-sa"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.service_account_id))
    error_message = "service_account_id must be a valid service account ID."
  }
}

variable "workload_identity_principal" {
  type        = string
  description = "Principal allowed to impersonate the service account via Workload Identity (e.g. principal://...). Empty to disable."
  default     = ""

  validation {
    condition     = var.workload_identity_principal == "" || can(regex("^principal", var.workload_identity_principal))
    error_message = "workload_identity_principal must be empty or start with 'principal'."
  }
}

variable "enable_workload_identity" {
  type        = bool
  description = "Whether to grant Workload Identity impersonation on the service account."
  default     = false
}