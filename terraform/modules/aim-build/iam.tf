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


#Reduce the scope of the following admin role.  It is included here to make it easier for developers to prototype new functionality.
resource "aws_iam_role_policy" "admin_policy" {
  name = "admin-role"
  role = data.aws_iam_role.example.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "*",
        "Resource": "*"
      }
    ]
  }
  EOF
}


resource "aws_iam_role_policy" "images_policy" {
  name = "images-role"
  role = data.aws_iam_role.example.id

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "imagebuilder:*"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "sns:ListTopics"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "sns:Publish"
        ],
        "Resource": "arn:aws:sns:*:*:*imagebuilder*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "license-manager:ListLicenseConfigurations",
          "license-manager:ListLicenseSpecificationsForResource"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "iam:GetRole"
        ],
        "Resource": "arn:aws:iam::*:role/aws-service-role/imagebuilder.amazonaws.com/AWSServiceRoleForImageBuilder"
      },
      {
        "Effect": "Allow",
        "Action": [
          "iam:GetInstanceProfile"
        ],
        "Resource": "arn:aws:iam::*:instance-profile/*imagebuilder*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "iam:ListInstanceProfiles",
          "iam:ListRoles"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": [
          "arn:aws:iam::*:instance-profile/*imagebuilder*",
          "arn:aws:iam::*:role/*imagebuilder*"
        ],
        "Condition": {
          "StringEquals": {
            "iam:PassedToService": "ec2.amazonaws.com"
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListAllMyBuckets",
          "s3:GetBucketLocation"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:ListBucket"
        ],
        "Resource": "arn:aws:s3::*:*imagebuilder*"
      },
      {
        "Action": "iam:CreateServiceLinkedRole",
        "Effect": "Allow",
        "Resource": "arn:aws:iam::*:role/aws-service-role/imagebuilder.amazonaws.com/AWSServiceRoleForImageBuilder",
        "Condition": {
          "StringLike": {
            "iam:AWSServiceName": "imagebuilder.amazonaws.com"
          }
        }
      },
      {
        "Effect": "Allow",
        "Action": [
          "ec2:DescribeImages",
          "ec2:DescribeVpcs",
          "ec2:DescribeRegions",
          "ec2:DescribeVolumes",
          "ec2:DescribeSubnets",
          "ec2:DescribeKeyPairs",
          "ec2:DescribeSecurityGroups"
        ],
        "Resource": "*"
      }
    ]
  }
  EOF
}