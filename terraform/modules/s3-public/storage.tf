## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

resource "aws_s3_bucket" "tf" {
  bucket = var.s3BucketNameTF
  acl    = "private"
  versioning { enabled = true }
  #Also add replication and encryption
}

#The following blocks every access except through the VPC endpoint and the static public IP of the agent or DevBox from which this Terraform program is run.  
#Note that the list of authorized IPs will need to be managed separately from within the VPC through the endpoint.  
#Also note that the public IP of the agent or devbox might be dynamic and thus the value passed here might become outdated.  
resource "aws_s3_bucket_policy" "b" {
  bucket = aws_s3_bucket.tf.id
  policy = <<POLICY
{
   "Version": "2012-10-17",
   "Id": "Policy1415115909152",
   "Statement": [
     {
       "Sid": "Access-to-admin-ip-only",
       "Principal": "*",
       "Action": "s3:*",
       "Effect": "Deny",
       "Resource": ["arn:aws:s3:::${var.s3BucketNameTF}",
                    "arn:aws:s3:::${var.s3BucketNameTF}/*"],
       "Condition": {
         "NotIpAddress": {
             "aws:SourceIp": [
                 "${var.adminPublicIP}"
             ]
         }
       }
     }
   ]
}
POLICY
}
