## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    
  
module "sg-rule" {  
  source = "../../modules/sg-rule"  
  #source = "..\\..\\modules\\sg-rule"  
  
  _region = var.aws_region  
  access_key = var._public_access_key  
  secret_access_key = var._secret_access_key  
  vpcName = var.vpcName  
  vpcId = var.vpcId  
  vpcCidr = var.vpcCidr  
  sgId = var.sgId  
  sgName = var.sgName  
  ruleType = var.ruleType  
  fromPort = var.fromPort  
  toPort = var.toPort  
  cidrBlocks = var.cidrBlocks  
  
}  

##Input variables
variable "aws_region" { }  
variable "_public_access_key" { }  
variable "_secret_access_key" { }  
variable "vpcName" { }
variable "vpcId" { }  
variable "vpcCidr" { }
variable "sgId" { }  
variable "sgName" { } 
variable "ruleType" { } 
variable "fromPort" { } 
variable "toPort" { } 
variable "cidrBlocks" { } 
