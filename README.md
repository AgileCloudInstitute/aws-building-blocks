# terraform-aws-simple-example  
Working example of creating basic aws instrustructure including EC2 VM in VPC  
    
##  This repo can either be:  
1.  consumed into a pipeline system as we will do with some of our examples  
2.  or cloned manually as a simple hands-on experience of using Terraform with AWS  
  
#  To use this manually:  
1.  Clone onto a machine on which Terraform has already been installed.  
2.  Copy the contents of the `Move-This-Directory-Outside-Of-Application-Path` directory to a different location so that any sensitive information like keys that you will put into it will NOT be transported around with the application code.  
3.  In the `VarsForTerraform/awspublickey.tfvars` file, place the AWS public key and AWS secret key for the AWS account that you will be using to instantiate this example.  
4.  In the `VarsForTerraform/awsvpcmeta.tfvars` file, put the correct abbreviation for the region in which you want your test resources to be created.  
5.  Open a terminal and navigate to the root directory into which you cloned this repository, then continue navigating to the `calls-to-modules\terraform-aws-simple-example-call-to-module` subdirectory.  
6.  Type `terraform init` to initialize the local backend you will be using for this exercise.  
7.  Note the actual full path to the directory into which you placed your sensitive key files, then type the following command to create the infrastructure: `terraform apply -var-file=C:\path\to\secret-var\files\awspublickey.tfvars -var-file=C:\path\to\secret-var\files\awsvpcmeta.tfvars`  
8.  Review the changes that terraform will tell you it will make, then type `yes` to approve.  Watch the resources be created.  
9.  Note the IP address that is printed in the console as an output variable.  
10.  If on windows, open a Putty instance.  Putty to the IP address of the newly created EC2 instance, which was given as an output variable when the `terraform apply` command was run.  Then login with the username and password that you put in the `userdata.tf` file.  
11.  If on Linux, `ssh` to the IP address of the instance using the username you specified in the USERDATA.  
13.  Change your password immediately upon logging in by typing the commands given below.  Write down your replacement password somewhere safe so that you remember it.  Again note that putting a password in USERDATA is bad practice.  We are only doing it here to keep this example very simple.  
    
        $ passwd  
        Changing password for user aci-user.  
        Changing password for aci-user.  
        (current) UNIX password:  
        New password:  
        Retype new password:  
        passwd: all authentication tokens updated successfully.  
        $  
      
#  Destroy the infrastructure you created above in order to avoid paying for what you do not use:  
1.  Return to the console window in which you typed the `apply` command above.  Make sure it is pointed to the same directory in which you ran the `apply` command.  
2.  Type the following `destroy` command, remembering to use the same path for the variable files that you used when applying above.  You can simply replace the word `apply` with the word `destroy`  as follows:  `terraform destroy -var-file=C:\path\to\secret-var\files\awspublickey.tfvars -var-file=C:\path\to\secret-var\files\awsvpcmeta.tfvars`    
  
