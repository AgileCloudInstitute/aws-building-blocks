## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

provider "aws" {
  region     = "us-west-2"
  access_key = var.access_key
  secret_key = var.secret_access_key

}

# Not required: currently used in conjuction with using icanhazip.com to determine local workstation external IP
provider "http" {}

