## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

module "terraform-aws-simple-example" {
  source = "../../modules/terraform-aws-simple-example-module"
  #source = "..\\..\\modules\\terraform-aws-simple-example-module"

  _region = "us-west-2"
  access_key = "${var._public_access_key}"
  secret_access_key = "${var._secret_access_key}"
  #path_to_ssh_keys = "${var.path_to_ssh_keys}"
  #name_of_ssh_key = "${var.name_of_ssh_key}"

}

##Input variables
variable "aws_region" { }
variable "_public_access_key" { }
variable "_secret_access_key" { }
#variable "path_to_ssh_keys" { }
#variable "name_of_ssh_key" { }

##Output variables
output "public_ip_of_ec2_instance" { value = "${module.terraform-aws-simple-example.public_ip_of_ec2_instance}" }
