## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

#This file first retrieves the IAM role that is attached to the instance profile we are 
#using and then attaches a new role policy to that instance profile so that the instance's 
#userdata can retrieve the password from the secrets manager.
#Note that iamRoleName is arbitrarily chosen, so that input config must ensure it refers 
#to the role that is attached to the launch config.

data "aws_iam_role" "example" {
  name = var.iamRoleName
}


resource "aws_iam_role_policy" "secrets_policy" {
  name = "secrets-role"
  role = data.aws_iam_role.example.id

  policy = <<-EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "*"
          }
      ]
  }
  EOF
}
