import subprocess

path_to_input_vars="C:\\projects\\terraform-simple-aws-example\\vars\\VarsForTerraform\\"

subprocess.run("terraform destroy -auto-approve -var-file="+path_to_input_vars+"awspublickey.tfvars -var-file="+path_to_input_vars+"awsvpcmeta.tfvars -var-file="+path_to_input_vars+"awskeymeta.tfvars", shell=True, check=True)
