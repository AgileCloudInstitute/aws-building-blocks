## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# Using these data sources allows the configuration to be generic for any region.
data "aws_region" "current" {}
data "aws_availability_zones" "available" {}

############Input variables
variable "access_key" { }  
variable "secret_access_key" { }  
variable "_region" { }  
variable "vpcId" { }  
variable "cidrSubnet" { }  
variable "cidrBlocks" { }  
  
#############Output variables
output "subnet_id" { value = aws_subnet.example-host.id }
output "sg_id" { value = aws_security_group.subnet-group-vm.id }