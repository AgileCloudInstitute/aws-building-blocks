## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "aws-iam" {
  #source = "../../modules/aws-iam"
  source = "..\\..\\..\\modules\\aws-iam"

  access_key = var.access_key
  secret_access_key = var.secret_access_key
  _region = var._region

}

##Input variables
variable "access_key" { }
variable "secret_access_key" { }
variable "_region" { }
  
##Output variables
output "encrypted_secret" { value = module.aws-iam.secret }
