## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# VPC Resources ( VPC, Subnets, Internet Gateway, Route Table )

resource "aws_vpc" "example-host" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = "1"
  tags = { Name = "example-host" }
}

resource "aws_subnet" "example-host" {
  depends_on = [aws_vpc.example-host]
  availability_zone = data.aws_availability_zones.available.names[0]
  cidr_block        = "10.0.0.0/24"
  vpc_id            = aws_vpc.example-host.id
}

resource "aws_internet_gateway" "example-host" {
  depends_on = [aws_vpc.example-host]
  vpc_id = aws_vpc.example-host.id
}

resource "aws_route_table" "example-host" {
  depends_on = [aws_vpc.example-host]
  vpc_id = aws_vpc.example-host.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.example-host.id
  }
}

resource "aws_route_table_association" "example-host" {
  depends_on = [aws_subnet.example-host, aws_route_table.example-host]
  subnet_id      = aws_subnet.example-host.id
  route_table_id = aws_route_table.example-host.id
}
