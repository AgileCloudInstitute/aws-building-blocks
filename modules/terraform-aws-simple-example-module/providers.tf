
provider "aws" {
  region     = "us-west-2"
  access_key = var.access_key
  secret_key = var.secret_access_key

}

# Not required: currently used in conjuction with using icanhazip.com to determine local workstation external IP
provider "http" {}

