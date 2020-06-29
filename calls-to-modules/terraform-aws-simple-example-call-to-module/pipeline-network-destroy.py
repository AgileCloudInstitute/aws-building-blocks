## Copyright 2020 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

import subprocess  
import sys  
import os  
  
region=sys.argv[1]  
print("region variable is: ")  
print(region)  

print("public key is: ")
print(os.environ['AWS_PUB'])
print("secret key is: ")
print(os.environ['AWS_SECRET'])

destroyCommand="terraform destroy -auto-approve -var 'aws_region="+region+"' -var '_public_access_key="+os.environ['AWS_PUB']+"' -var '_secret_access_key="+os.environ['AWS_SECRET']+"'"

subprocess.run(destroyCommand, shell=True, check=True)
