## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    
  
####################################################  
# Below we create the USERDATA to get the instance ready to run.
# The Terraform local simplifies Base64 encoding.  
locals {

  example-host-userdata = <<USERDATA
#!/bin/bash -e

/usr/sbin/useradd "${var.vm_username}"

echo "${var.vm_username}":$(aws secretsmanager get-secret-value --secret-id "${var.vm_username}" --version-stage AWSCURRENT --region "${var._region}" --output text --query SecretString) | chpasswd

echo '"${var.vm_username}" ALL=(ALL:ALL) ALL' | sudo EDITOR='tee -a' visudo
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd

#Review this link when planning a more secure password handling process: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret

mkdir /home/"${var.vm_username}"/cloned-repos
mkdir /home/"${var.vm_username}"/vars
mkdir /home/"${var.vm_username}"/staging

chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/vars
chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/cloned-repos
chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/staging

### Install software
yum -y update
sudo yum install git -y

echo "About to install python3"
sudo yum install -y python3
sudo yum install -y python3-setuptools

##Put any other startup commands you want to put here.
##Remember there are other approaches such as configuration tools like Ansible, Chef, Puppet, etc.


USERDATA

}