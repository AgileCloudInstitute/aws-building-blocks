## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess  
import sys  
import os  
  
region=sys.argv[1]  
print("region variable is: ")  
print(region)  

#'_public_access_key=$AWS_PUB'
#'_secret_access_key=$AWS_SECRET'
print("public key is: ")
print(os.environ['AWS_PUB'])
print("secret key is: ")
print(os.environ['AWS_SECRET'])
#'aws_region=region'

#path_to_input_vars="C:\\projects\\terraform-simple-aws-example\\vars\\VarsForTerraform\\"

#subprocess.run("terraform init", shell=True, check=True)

#subprocess.run("terraform apply -auto-approve -var-file="+path_to_input_vars+"awspublickey.tfvars -var-file="+path_to_input_vars+"awsvpcmeta.tfvars -var-file="+path_to_input_vars+"awskeymeta.tfvars", shell=True, check=True)

#subprocess.run("terraform apply -auto-approve 
#               -var-file="+path_to_input_vars+"awspublickey.tfvars 
#               -var-file="+path_to_input_vars+"awsvpcmeta.tfvars 
#               -var-file="+path_to_input_vars+"awskeymeta.tfvars"
#               , shell=True, check=True)
