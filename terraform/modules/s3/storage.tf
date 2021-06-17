## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

resource "aws_kms_key" "mykey" {
  description             = "This key is used to encrypt bucket objects"
  #If you delete the key in KMS, the key will only remain recoverable for the number of days specified in the next line.  After the key is no longer recoverable, the data in the bucket will be lost forever.  But if you do not delete the key, the data will remain available until you delete the data explicitly.  
  deletion_window_in_days = 10
}

resource "aws_s3_bucket" "tf" {

  bucket = var.s3BucketNameTF
  acl = "aws-exec-read"

  versioning {
    enabled = true
  }

  #Also add replication
}

resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.selected.id 
  service_name = "com.amazonaws.us-west-2.s3"
  
  tags = {  
    Environment = var.environmentName  
	System = var.systemName  
	Owner = var.ownerName  
  }  

}

resource "aws_vpc_endpoint_route_table_association" "example" {
  count = length(tolist(data.aws_route_tables.rts.ids))
  route_table_id = tolist(data.aws_route_tables.rts.ids)[count.index]
  vpc_endpoint_id = aws_vpc_endpoint.s3.id
}

resource "aws_dynamodb_table" "terraform-lock" {
    name           = var.dynamoDbTableNameTF
    read_capacity  = 5
    write_capacity = 5
    hash_key       = "LockID"
    attribute {
        name = "LockID"
        type = "S"
    }
    tags = {
        "Name" = "DynamoDB Terraform State Lock Table"
    }
}

data "aws_iam_role" "example" {
  name = var.iamRoleName
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "storage-policy"
  role = data.aws_iam_role.example.id

  policy = <<-EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "s3:PutAnalyticsConfiguration",
                  "s3:GetObjectVersionTagging",
                  "s3:CreateBucket",
                  "s3:ReplicateObject",
                  "s3:GetObjectAcl",
                  "s3:GetBucketObjectLockConfiguration",
                  "s3:DeleteBucketWebsite",
                  "s3:PutLifecycleConfiguration",
                  "s3:GetObjectVersionAcl",
                  "s3:DeleteObject",
                  "s3:GetBucketPolicyStatus",
                  "s3:GetObjectRetention",
                  "s3:GetBucketWebsite",
                  "s3:PutReplicationConfiguration",
                  "s3:PutObjectLegalHold",
                  "s3:GetObjectLegalHold",
                  "s3:GetBucketNotification",
                  "s3:PutBucketCORS",
                  "s3:GetReplicationConfiguration",
                  "s3:ListMultipartUploadParts",
                  "s3:PutObject",
                  "s3:GetObject",
                  "s3:PutBucketNotification",
                  "s3:PutBucketLogging",
                  "s3:GetAnalyticsConfiguration",
                  "s3:PutBucketObjectLockConfiguration",
                  "s3:GetObjectVersionForReplication",
                  "s3:GetLifecycleConfiguration",
                  "s3:GetInventoryConfiguration",
                  "s3:GetBucketTagging",
                  "s3:PutAccelerateConfiguration",
                  "s3:DeleteObjectVersion",
                  "s3:GetBucketLogging",
                  "s3:ListBucketVersions",
                  "s3:RestoreObject",
                  "s3:ListBucket",
                  "s3:GetAccelerateConfiguration",
                  "s3:GetBucketPolicy",
                  "s3:PutEncryptionConfiguration",
                  "s3:GetEncryptionConfiguration",
                  "s3:GetObjectVersionTorrent",
                  "s3:AbortMultipartUpload",
                  "s3:GetBucketRequestPayment",
                  "s3:DeleteBucketOwnershipControls",
                  "s3:GetObjectTagging",
                  "s3:GetMetricsConfiguration",
                  "s3:GetBucketOwnershipControls",
                  "s3:DeleteBucket",
                  "s3:PutBucketVersioning",
                  "s3:GetBucketPublicAccessBlock",
                  "s3:ListBucketMultipartUploads",
                  "s3:PutMetricsConfiguration",
                  "s3:PutBucketOwnershipControls",
                  "s3:GetBucketVersioning",
                  "s3:GetBucketAcl",
                  "s3:PutInventoryConfiguration",
                  "s3:GetObjectTorrent",
                  "s3:PutBucketWebsite",
                  "s3:PutBucketRequestPayment",
                  "s3:PutObjectRetention",
                  "s3:GetBucketCORS",
                  "s3:GetBucketLocation",
                  "s3:ReplicateDelete",
                  "s3:GetObjectVersion"
              ],
              "Resource": [
                  "arn:aws:s3:::${var.s3BucketNameTF}",
                  "arn:aws:s3:::${var.s3BucketNameTF}/*"
              ]
          },
          {
              "Sid": "VisualEditor1",
              "Effect": "Allow",
              "Action": [
                  "s3:ListStorageLensConfigurations",
                  "s3:GetAccessPoint",
                  "s3:GetAccountPublicAccessBlock",
                  "s3:ListAllMyBuckets",
                  "s3:ListAccessPoints",
                  "s3:ListJobs",
                  "s3:PutStorageLensConfiguration",
                  "s3:CreateJob"
              ],
              "Resource": "*"
          }
      ]
  }
  EOF
}

resource "aws_iam_role_policy" "kms_policy" {
  name = "kms-role"
  role = data.aws_iam_role.example.id

  policy = <<-EOF
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "kms:GetParametersForImport",
                  "kms:GetPublicKey",
                  "kms:Decrypt",
                  "kms:GetKeyRotationStatus",
                  "kms:GetKeyPolicy",
                  "kms:GenerateDataKey",
                  "kms:DescribeKey",
                  "kms:ListResourceTags",
                  "kms:ScheduleKeyDeletion"
              ],
              "Resource": "${aws_kms_key.mykey.arn}"
          },
          {
              "Sid": "VisualEditor1",
              "Effect": "Allow",
              "Action": "kms:DescribeCustomKeyStores",
              "Resource": "*"
          }
      ]
  }
  EOF
}

data "aws_route_tables" "rts" {
  vpc_id = var.vpcId
}
