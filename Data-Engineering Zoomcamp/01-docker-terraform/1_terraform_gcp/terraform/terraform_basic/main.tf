terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  # credentials = "../../keys/gcp-cred.json"
  project     = "terrform-demo-412419"
  region      = "us-central1"
  zone        = "us-central1-c"

}


resource "google_storage_bucket" "terra-demo" {
  name          = "terrform-demo-412419-bucket"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
