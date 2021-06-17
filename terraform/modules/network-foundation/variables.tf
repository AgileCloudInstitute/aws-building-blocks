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
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }

#############Output variables
output "vpc_id" { value = aws_vpc.example-host.id }  
output "vpc_cidr" { value = aws_vpc.example-host.cidr_block }
output "sg_id" { value = aws_security_group.example-hosts.id }  
output "sg_name" { value = aws_security_group.example-hosts.name }  
output "instance_profile_name" { value = aws_iam_instance_profile.example-instance-profile.name }  
output "iam_role_name" { value = aws_iam_role.example-iam-role.name }
