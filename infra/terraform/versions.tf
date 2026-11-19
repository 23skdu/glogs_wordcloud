terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # Configure a remote backend for production use, e.g.:
  # backend "gcs" {
  #   bucket = "your-tf-state-bucket"
  #   prefix = "glogs-wordcloud"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}