## Copyright 2021 Green River IT (GreenRiverIT.com) as described in LICENSE.txt distributed with this project on GitHub.  
## Start at https://github.com/AgileCloudInstitute?tab=repositories    
  
resource "aws_secretsmanager_secret" "example2" {
  name = var.vm_username
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "test2" {
  secret_id     = aws_secretsmanager_secret.example2.id
  secret_string = var.vm_pwd
}

resource "aws_secretsmanager_secret" "example-cert" {
  name = "example-cert"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "cert-val" {
  secret_id     = aws_secretsmanager_secret.example-cert.id
  secret_binary = filebase64(var.certFileAndPath)
}

resource "aws_secretsmanager_secret" "example-key" {
  name = "example-key"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "key-val" {
  secret_id     = aws_secretsmanager_secret.example-key.id
  secret_binary = filebase64(var.keyFileAndPath)
}

resource "aws_secretsmanager_secret" "s3pubKey" {
  name = "s3pubKey"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "s3pubKeyVersion" {
  secret_id     = aws_secretsmanager_secret.s3pubKey.id
  secret_string = var.access_key
}

resource "aws_secretsmanager_secret" "s3secKey" {
  name = "s3secKey"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "s3secKeyVersion" {
  secret_id     = aws_secretsmanager_secret.s3secKey.id
  secret_string = var.secret_access_key
}
