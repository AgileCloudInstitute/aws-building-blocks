Put the `.pem` and `.ppk` files in this directory after you have moved this entire directory to a different location outside the application path.   

The `.pem` file will be uploaded automatically to the created VM by terraform if you reference the right source directory in the terraform code.  

The `.ppk` file you will use to putty into the EC2 instance after terraform creates the EC2 instance for you.  
