#IMPORTANT: Only use the below with a remote backend from pipeline.  
#IMPORTANT: If you are running this locally as a simple example, make sure to comment out or delete the below to force a local backend instead.
terraform {
  backend "azurerm" { }
}
