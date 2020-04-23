## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess

path_to_input_vars="C:\\projects\\terraform-simple-aws-example\\vars\\VarsForTerraform\\"

subprocess.run("terraform init", shell=True, check=True)

subprocess.run("terraform apply -auto-approve -var-file="+path_to_input_vars+"awspublickey.tfvars -var-file="+path_to_input_vars+"awsvpcmeta.tfvars -var-file="+path_to_input_vars+"awskeymeta.tfvars", shell=True, check=True)
