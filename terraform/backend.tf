terraform {
  backend "s3" {
    bucket = "tf-state-eu-south-1"
    key    = "private-geo-proxy/terraform.tfstate"
    region = "eu-south-1"
  }
}
