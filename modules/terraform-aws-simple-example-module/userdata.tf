## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    
  
####################################################  
# Below we create the USERDATA to get the instance ready to run.
# The Terraform local simplifies Base64 encoding.  
locals {

  example-host-userdata = <<USERDATA
#!/bin/bash -xe

#SECURITY HOLE: Just for easy demonstration, the following enables password login and creates an aci-user with a password exposed in version control. 
#Replace the following 4 lines with something more secure when you establish a secrets management system.
/usr/sbin/useradd aci-user
echo aci-user:just-for-demo123 | chpasswd
echo 'aci-user ALL=(ALL:ALL) ALL' | sudo EDITOR='tee -a' visudo
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart sshd

mkdir /home/aci-user/cloned-repos
mkdir /home/aci-user/vars

chown -R aci-user:aci-user /home/aci-user/vars
chown -R aci-user:aci-user /home/aci-user/cloned-repos

### Install software
yum -y update
sudo yum install git -y

echo "About to install python3"
sudo yum install -y python3
sudo yum install -y python3-setuptools
sudo easy_install-3.7 pip

##Put any other startup commands you want to put here.
##Remember there are other approaches such as configuration tools like Ansible, Chef, Puppet, etc.

USERDATA

}