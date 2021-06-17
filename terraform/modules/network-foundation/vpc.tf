## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

resource "aws_vpc" "example-host" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = "1"
  tags = {
    Name = var.vpcName
    System = var.systemName
    Environment = var.environmentName
    Owner = var.ownerName
  }
}

resource "aws_internet_gateway" "example-host" {
  depends_on = [aws_vpc.example-host]
  vpc_id = aws_vpc.example-host.id
}

resource "aws_route_table" "example-host" {
  depends_on = [aws_vpc.example-host]
  vpc_id = aws_vpc.example-host.id

  tags = {
    NameOfTable = "example-host"
  }

}

resource "aws_route" "r" {
  route_table_id = aws_route_table.example-host.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.example-host.id
  depends_on = [aws_route_table.example-host]
}

resource "aws_security_group" "example-hosts" {
  name        = "example node"
  description = "Security group"
  vpc_id      = aws_vpc.example-host.id  

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_instance_profile" "example-instance-profile" {
  name = "example-instance-profile"
  role = aws_iam_role.example-iam-role.name
}

resource "aws_iam_role" "example-iam-role" {
  name = "example-iam-role"

  assume_role_policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  }
  EOF
}
