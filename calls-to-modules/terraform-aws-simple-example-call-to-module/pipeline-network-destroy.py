## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess  
import sys  
import os  
  
region=sys.argv[1]  
print("region variable is: ")  
print(region)  

path_to_ssh_keys=sys.argv[2]
print("path_to_ssh_keys is: ")
print(path_to_ssh_keys)

name_of_ssh_key=sys.argv[3]
print("name_of_ssh_key is: ")
print(name_of_ssh_key)

print("public key is: ")
print(os.environ['AWS_PUB'])
print("secret key is: ")
print(os.environ['AWS_SECRET'])

destroyCommand="terraform apply -auto-approve -var 'aws_region="+region+"' -var 'path_to_ssh_keys="+path_to_ssh_keys+"' -var 'name_of_ssh_key="+name_of_ssh_key+"' -var '_public_access_key="+os.environ['AWS_PUB']+"' -var '_secret_access_key="+os.environ['AWS_SECRET']+"'"

subprocess.run(destroyCommand, shell=True, check=True)
