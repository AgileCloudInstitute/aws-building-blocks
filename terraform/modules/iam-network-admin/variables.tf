## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

variable "access_key" { }
variable "secret_access_key" { }
variable "_region" { }

output "secret" {
  value = aws_iam_access_key.lb.encrypted_secret
}
# secret_access_key may be decrypted by typing: terraform output encrypted_secret | base64 --decode | keybase pgp decrypt  
