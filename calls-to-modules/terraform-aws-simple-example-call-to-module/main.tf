## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "terraform-aws-simple-example" {
  source = "../../modules/terraform-aws-simple-example-module"
  #source = "..\\..\\modules\\terraform-aws-simple-example-module"

  _region = "${var.aws_region}"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  vpcName = "${var.vpcName}"
  systemName = "${var.systemName}"
  environmentName = "${var.environmentName}"
  ownerName = "${var.ownerName}"
  vmName = "${var.vmName}"

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
variable "vpcName" { }
variable "systemName" { }
variable "environmentName" { }
variable "ownerName" { }
variable "vmName" { }

##Output variables
output "public_ip_of_ec2_instance" { value = "${module.terraform-aws-simple-example.public_ip_of_ec2_instance}" }
