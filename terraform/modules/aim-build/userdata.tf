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
service sshd restart

mkdir /home/"${var.vm_username}"/cloned-repos
mkdir /home/"${var.vm_username}"/vars
mkdir /home/"${var.vm_username}"/staging

chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/vars
chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/cloned-repos
chown -R "${var.vm_username}":"${var.vm_username}" /home/"${var.vm_username}"/staging

### Install software
yum -y update
sudo yum install git -y

##Put any other startup commands you want to put here.
##Remember there are other approaches such as configuration tools like Ansible, Chef, Puppet, etc.

#Add code to set up the ami tools from this link:  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-up-ami-tools.html
yum install -y ruby
wget https://s3.amazonaws.com/ec2-downloads/ec2-ami-tools.noarch.rpm
rpm -K ec2-ami-tools.noarch.rpm
rpm -Kv ec2-ami-tools.noarch.rpm
yum install -y ec2-ami-tools.noarch.rpm
export RUBYLIB=$RUBYLIB:/usr/lib/ruby/site_ruby:/usr/lib64/ruby/site_ruby

cat <<'EOF'>/etc/profile.d/ec2-ami-tools.sh
export PATH=$PATH:/usr/local/bin/
export RUBYLIB=$RUBYLIB:/usr/lib/ruby/site_ruby:/usr/lib64/ruby/site_ruby
EOF

source /etc/profile.d/ec2-ami-tools.sh

echo '\\nNow check the version of ec2-ami-tools that is installed\\n'
ec2-ami-tools-version

echo "Create directory into which to save the credentials that will be imported from the secrets manager."
mkdir /tmp/cert

echo "Finally, import the two key files from the secrets manager..."
echo "First save the cert."
echo $(aws secretsmanager get-secret-value --secret-id "example-cert" --version-stage AWSCURRENT --region "${var._region}" --output text --query SecretBinary) | base64 -d >> /tmp/cert/myCert.pem

echo "Then save the key."
echo $(aws secretsmanager get-secret-value --secret-id "example-key" --version-stage AWSCURRENT --region "${var._region}" --output text --query SecretBinary) | base64 -d >> /tmp/cert/myKey.pem

echo "Then get account number.  "
echo $(aws sts get-caller-identity --query Account --output text)

#Note fore ebs backed image do not use ec2-bundle-vol and also remove above installation of required things like ruby.
echo "Then create the AMI bundle: "
ec2-bundle-vol -k /tmp/cert/myKey.pem -c /tmp/cert/myCert.pem -u $(aws sts get-caller-identity --query Account --output text) -r x86_64 -e /tmp/cert --partition gpt 

# Upload to s3
echo "Now upload the image to s3. "
ec2-upload-bundle -b demoxyz123wergwej7/images/instance_backed_amznlnx1 -m /tmp/image.manifest.xml -a $(aws secretsmanager get-secret-value --secret-id "s3pubKey" --version-stage AWSCURRENT --region "${var._region}" --output text --query SecretString) -s $(aws secretsmanager get-secret-value --secret-id "s3secKey" --version-stage AWSCURRENT --region "${var._region}" --output text --query SecretString) --region "${var._region}"  

echo "Now register the AMI."
aws ec2 register-image --image-location demoxyz123wergwej7/images/instance_backed_amznlnx1/image.manifest.xml --name instance_backed_amznlnx1 --virtualization-type hvm --region "${var._region}" --debug 

echo "Now remove the bundle from the tmp directory. "
sudo rm /tmp/image.manifest.xml /tmp/image.part.* /tmp/image

echo "\\nDone with userdata script.\\n"

USERDATA

}