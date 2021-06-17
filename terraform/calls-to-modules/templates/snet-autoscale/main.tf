## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "snet-autoscale" {
  #source = "../../modules/snet-autoscale"
  source = "..\\..\\modules\\snet-autoscale"

  access_key = var.access_key
  secret_access_key = var.secret_access_key
  _region = var._region
  vpcId = var.vpcId
  systemName = var.systemName
  environmentName = var.environmentName
  ownerName = var.ownerName
  vmName = var.vmName
  cidrSubnet = var.cidrSubnet
  instanceProfileName = var.instanceProfileName
  iamRoleName = var.iamRoleName
  vm_username = var.vm_username
  vm_pwd = var.vm_pwd
  placementStrategy = var.placementStrategy
  image_name = var.image_name
  image_architecture = var.image_architecture

}

##Input variables
variable "access_key" { }  
variable "secret_access_key" { }  
variable "_region" { }  
variable "vpcId" { }  
variable "systemName" { }  
variable "environmentName" { }  
variable "ownerName" { }  
variable "vmName" { }  
variable "cidrSubnet" { }  
variable "instanceProfileName" { }
variable "iamRoleName" { }
variable "vm_username" { }
variable "vm_pwd" { }
variable "placementStrategy" { }
variable "image_name" { }
variable "image_architecture" { }
