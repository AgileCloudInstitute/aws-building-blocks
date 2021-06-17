## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "s3" {
  source = "../../modules/s3"
  #source = "..\\..\\modules\\s3"

  _region = var.aws_region
  access_key = var._public_access_key
  secret_access_key = var._secret_access_key
  vpcId = var.vpcId
  systemName = var.systemName
  environmentName = var.environmentName
  ownerName = var.ownerName
  s3BucketNameTF = var.s3BucketNameTF
  dynamoDbTableNameTF = var.dynamoDbTableNameTF
  iamRoleName = var.iamRoleName
  adminPublicIP = var.adminPublicIP
}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcId" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }
variable "s3BucketNameTF" { }
variable "dynamoDbTableNameTF" { } 
variable "iamRoleName" { }
variable "adminPublicIP" { }
