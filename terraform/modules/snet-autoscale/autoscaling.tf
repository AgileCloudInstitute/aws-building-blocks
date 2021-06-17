## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

resource "aws_autoscaling_group" "asg-template" {
  name                 = "asg-template"
  desired_capacity     = 1
  max_size             = 1
  min_size             = 1
  placement_group      = aws_placement_group.web.id
  launch_template {
    id      = aws_launch_template.example-launch-template.id
    version = aws_launch_template.example-launch-template.latest_version
  }

  vpc_zone_identifier  = [aws_subnet.example-host.id]

  #Consider adding an initial_lifecycle_hook to ensure that roles have been applied
}


resource "aws_placement_group" "web" {
  name     = "example-pg"
  strategy = var.placementStrategy
}


resource "aws_launch_template" "example-launch-template" {
  name = "example-launch-template"
  iam_instance_profile { name = var.instanceProfileName }
  image_id = data.aws_ami.amazon-linux-2.id
  instance_initiated_shutdown_behavior = "terminate"
  instance_type = "t2.micro"
  monitoring { enabled = true }
  network_interfaces { 
    associate_public_ip_address = true 
    security_groups = [aws_security_group.subnet-group-autoscaling.id]
  }
  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = var.vmName
      System = var.systemName
      Environment = var.environmentName
      Owner = var.ownerName
    }
  }
  user_data = base64encode(local.example-host-userdata)
}

data "aws_caller_identity" "current" {}

data "aws_ami" "amazon-linux-2" {  
  most_recent = true
  
  owners = [data.aws_caller_identity.current.account_id]
 
  filter {
    name   = "name"
    values = [var.image_name]
  }
  
  filter {
    name   = "architecture"
    values = [var.image_architecture]
  }

}  
