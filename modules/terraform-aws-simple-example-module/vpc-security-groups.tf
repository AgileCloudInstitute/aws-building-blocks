## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# Security group and rule to allow the node to communicate with the outside world.  

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

resource "aws_security_group_rule" "example-admin-ssh" {
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks       = ["${local.admin-external-cidr}"]
  security_group_id        = aws_security_group.example-hosts.id
}
