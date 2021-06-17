## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "snet-packer" {
  #source = "../../modules/snet-packer"
  source = "..\\..\\modules\\snet-packer"

  _region = var.aws_region
  access_key = var._public_access_key
  secret_access_key = var._secret_access_key
  vpcId = var.vpcId
  cidrSubnet = var.cidrSubnet
  cidrBlocks = var.cidrBlocks

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcId" { }
variable "cidrSubnet" { }  
variable "cidrBlocks" { }
  
##Output variables
output "subnet_id" { value = module.snet-packer.subnet_id }
output "sg_id" { value = module.snet-packer.sg_id }