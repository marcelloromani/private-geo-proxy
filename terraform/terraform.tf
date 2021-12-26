terraform {
  required_version = "~> 1.1.2"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.50.0"
    }
  }

  backend "s3" {
    bucket  = "tf-state-eu-south-1"
    key     = "private-geo-proxy/terraform.tfstate"
    encrypt = false
    region  = "eu-south-1"
  }
}

provider "aws" {
  region = "eu-south-1"

  default_tags {
    tags = {
      ManagedBy = "Terraform"
    }
  }
}
