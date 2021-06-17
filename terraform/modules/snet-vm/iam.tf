## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

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
