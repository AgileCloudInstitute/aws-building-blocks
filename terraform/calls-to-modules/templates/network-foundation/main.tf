## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "aws-network-foundation" {
  #source = "../../modules/aws-network-foundation"
  source = "..\\..\\modules\\aws-network-foundation"

  _region = var.aws_region
  access_key = var._public_access_key
  secret_access_key = var._secret_access_key
  vpcName = var.vpcName
  systemName = var.systemName
  environmentName = var.environmentName
  ownerName = var.ownerName

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcName" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }

##Output variables
output "vpc_id" { value = module.aws-network-foundation.vpc_id }
output "vpc_cidr" { value = module.aws-network-foundation.vpc_cidr }
output "sg_id" { value = module.aws-network-foundation.sg_id }
output "sg_name" { value = module.aws-network-foundation.sg_name }

output "instance_profile_name" { value = module.aws-network-foundation.instance_profile_name }  
output "iam_role_name" { value = module.aws-network-foundation.iam_role_name }
