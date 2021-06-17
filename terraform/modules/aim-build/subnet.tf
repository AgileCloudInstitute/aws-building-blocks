## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

data "aws_vpc" "selected" {
  id = var.vpcId
}

data "aws_route_table" "rt" {
  vpc_id = var.vpcId

  filter {
    #name   = "association.main"
    #values = [false]

    name   = "tag:NameOfTable"
    values = ["example-host"]

  }

}

resource "aws_subnet" "example-host" {
  #depends_on = [aws_vpc.example-host]
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block        = var.cidrSubnet
  vpc_id            = data.aws_vpc.selected.id
}

resource "aws_route_table_association" "example" {
  route_table_id = data.aws_route_table.rt.id
  subnet_id      = aws_subnet.example-host.id
}


resource "aws_security_group" "subnet-group-vm" {
  name        = "vm-subnet"
  description = "Security group"
  vpc_id      = data.aws_vpc.selected.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
