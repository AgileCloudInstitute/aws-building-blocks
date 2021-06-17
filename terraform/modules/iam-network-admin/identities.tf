## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    

# group starter_kit_admins 
resource "aws_iam_group" "starter_kit_admins" {
    name = "starter-kit-admins"
}
 
# create users
resource "aws_iam_user" "starter_kit_admin1" {
    name = "starter-kit-admin1"
}

resource "aws_iam_access_key" "lb" {
  user    = aws_iam_user.starter_kit_admin1.name
}

 
# add users to a group
resource "aws_iam_group_membership" "starter_kit_admins_users" {
    name = "starter-kit-admins-users"
    users = [ aws_iam_user.starter_kit_admin1.name ]
    group = aws_iam_group.starter_kit_admins.name
}
