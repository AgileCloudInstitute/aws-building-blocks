## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

data "aws_ami" "amazon-linux-2" {  
  most_recent = true
  
  owners = [var.image_owner]
 
  filter {
    name   = "name"
    values = [var.image_name]
  }
  
  filter {
    name   = "architecture"
    values = ["x86_64*"]
  }

}  
