## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# Using these data sources allows the configuration to be generic for any region.
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

############Input variables
variable "access_key" { }  
variable "secret_access_key" { }  
variable "_region" { }  
variable "vpcName" { }  
variable "vpcId" { }  
variable "vpcCidr" { }
variable "sgId" { }  
variable "sgName" { }  
variable "ruleType" { } 
variable "fromPort" { } 
variable "toPort" { } 
variable "cidrBlocks" { } 
  
data "aws_vpc" "example-vpc" { 
  id   = var.vpcId

  filter {
    name   = "cidr"
    values = [var.vpcCidr]
  }

}
