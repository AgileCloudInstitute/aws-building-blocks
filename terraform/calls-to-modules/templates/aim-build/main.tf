## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "aim-build" {
  #source = "../../modules/aim-build"
  source = "..\\..\\modules\\aim-build"

  _region = var.aws_region
  access_key = var._public_access_key
  secret_access_key = var._secret_access_key
  vpcId = var.vpcId
  systemName = var.systemName
  environmentName = var.environmentName
  ownerName = var.ownerName
  vmName = var.instanceName
  instanceProfileName = var.instanceProfileName
  iamRoleName = var.iamRoleName
  cidrSubnet = var.cidrSubnet
  vm_username = var.vm_username 
  vm_pwd = var.vm_pwd

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcId" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }
variable "instanceName" { }
variable "instanceProfileName" { }
variable "iamRoleName" { }
variable "cidrSubnet" { }  
variable "vm_username" { }
variable "vm_pwd" { }

##Output variables
output "public_ip_of_ec2_instance" { value = module.aim-build.public_ip_of_ec2_instance }
output "ami_id" { value = module.aim-build.ami_id }
