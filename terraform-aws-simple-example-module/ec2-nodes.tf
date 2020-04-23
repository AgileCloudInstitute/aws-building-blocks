
data "aws_ami" "amazon-linux-2" {  
  most_recent = true
  
  owners = ["amazon"]
 
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
  
  filter {
    name   = "architecture"
    values = ["x86_64*"]
  }

}  

resource "aws_instance" "example-host" {
  depends_on = [aws_internet_gateway.example-host]
  ami                         = data.aws_ami.amazon-linux-2.id
  associate_public_ip_address = true
  instance_type               = "t2.micro"
  key_name                    = var.name_of_ssh_key
  user_data_base64 = base64encode(local.example-host-userdata)
  source_dest_check           = false
  subnet_id = aws_subnet.example-host.id
  vpc_security_group_ids = [aws_security_group.example-hosts.id]

  connection {
    type        = "ssh"
    user        = "ec2-user"
    private_key = file("${var.path_to_ssh_keys}${var.name_of_ssh_key}.pem")
    host = self.public_ip
  }

  timeouts {
    create = "60m"
    update = "60m"
    delete = "60m"
  }
  
  tags = { Name = "Example-Host" }
}
