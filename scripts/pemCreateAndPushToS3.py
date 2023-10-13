from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime
from shutil import copyfile
import zipfile
import subprocess
import sys
import json
import os
import yaml
import platform

#PREREQUISITE
#MUST RUN: pip install cryptography

def generatePems():
  # Generate a private key
  private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=1024,
  )

  # Create a self-signed certificate
  subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Washington'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u'Seattle'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'MyOrg'),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'MyDept'),
    x509.NameAttribute(NameOID.COMMON_NAME, u'*.ec2.internal'),
  ])

  cert = x509.CertificateBuilder().subject_name(
    subject
  ).issuer_name(
    issuer
  ).public_key(
    private_key.public_key()
  ).serial_number(
    x509.random_serial_number()
  ).not_valid_before(
    datetime.datetime.utcnow()
  ).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
  ).sign(private_key, hashes.SHA256())

  # Save the private key and certificate to files
  with open("privateKey.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ))

  with open("certificateChain.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))
  #Please note that you’ll need to install the cryptography library to run this code. 
  # You can install it using pip install cryptography.

  #Create duplicate with different name
  copyfile("certificateChain.pem", "trustedCertificates.pem")

  # Zip the three new files into a single new file
  lista_files = ["certificateChain.pem","privateKey.pem","trustedCertificates.pem"]
  with zipfile.ZipFile('my-certs.zip', 'w') as zipMe:        
    for file in lista_files:
        zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

def runCliCommand(cmd):
  print("----------------------------------------------------")
  logString = "About to run cli command: "+cmd
  print(logString)
  process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  logString = "data string is: " + data
  print(logString)
  logString = "err is: " + str(err)
  print(logString)
  logString = "process.returncode is: " + str(process.returncode)
  print(logString)
  if process.returncode == 0:
    logString = str(data)
    print(logString)
    print("-------")
  else:
    logString = "process.returncode is not zero.  Halting program so you can diagnose the root cause of the problem.  "
    print(logString)
    sys.exit

def getAccount(cmd='aws sts get-caller-identity'):
  print("----------------------------------------------------")
  logString = "About to run cli command: "+cmd
  print(logString)
  process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  logString = "data string is: " + data
  print(logString)
  logString = "err is: " + str(err)
  print(logString)
  logString = "process.returncode is: " + str(process.returncode)
  print(logString)
  if process.returncode == 0:
    logString = str(data)
    print(logString)
    mydata = json.loads(data)
    if "Account" in mydata:
      myAccountId = mydata["Account"]
      print("Account Id is: ", myAccountId)
      if ((len(myAccountId)!=12) or (not str(myAccountId).isdigit())):
        logString = "An unexpected value ( "+str(myAccountId)+" ) was returned for the aws account id. Halting program so you can identify the root cause.  "
        print(logString)
        sys.exit(1)
      return myAccountId
    else:
      logString = "The 'Account' key is not included in the response.  Halting program so you can identify the root cause of the problem. "
      print(logString)
      sys.exit(1)
  else:
    logString = "The '"+cmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def deleteFiles():
  lista_files = ["certificateChain.pem","privateKey.pem","trustedCertificates.pem","my-certs.zip"]
  for thisFile in lista_files:
    print("About to delete local copy of ", thisFile)
    os.remove(thisFile)
    print("Finished deleting local copy of ", thisFile)

def find(d, tag):
    if tag in d:
        yield d[tag]

def createConfigAndCredentialsAWS():
  # The following assumes that you only have one set of AWS credentials in keys.yaml, and that they have the key names given below.  
  if platform.system() == "Windows":
    osChar = '\\'
  else:
    osChar = '/'
  keyFile = os.path.expanduser('~')+osChar+'acm'+osChar+'keys'+osChar+'starter'+osChar+'keys.yaml'
  print("keyFile is: ", keyFile)
  if os.path.isfile(keyFile):
    print(keyFile, " is a file. ") 
  stream = open(keyFile, 'r')
  data = yaml.load(stream, yaml.SafeLoader)
  access_key=''
  secret_key=''

  for val in find(data, 'AWSAccessKeyId'):
    access_key = "aws_access_key_id = "+val+"\n"
  for val in find(data, 'AWSSecretKey'):
    secret_key = "aws_secret_access_key = "+val+"\n"
  if access_key != '':
    pass
  else:
    quit("ERROR: AWSAccessKeyId was not found in keys.yaml.")
  if secret_key != '':
    pass
  else:
    quit("ERROR: AWSSecretKey was not found in keys.yaml.")
  credFile = os.path.expanduser('~')+osChar+'.aws'+osChar+'credentials'
  print("credFile is: ", credFile)
  if not os.path.isfile(credFile):
    print(credFile, " is NOT a file. ") 
    with open(credFile, 'w') as out_file:
      out_file.write("[default]\n")
      out_file.write(access_key)
      out_file.write(secret_key)
  acmConfigFile = os.path.expanduser('~')+osChar+'acm'+osChar+'keys'+osChar+'starter'+osChar+'config.yaml'
  print("acmConfigFile is: ", acmConfigFile)
  if os.path.isfile(acmConfigFile):
    print(acmConfigFile, " is a file. ") 
  stream = open(acmConfigFile, 'r')
  data = yaml.load(stream, yaml.SafeLoader)
  awsregion=''
  for val in find(data, 'region'):
    awsregion = "region = "+val+"\n"
  configFile = os.path.expanduser('~')+osChar+'.aws'+osChar+'config'
  print("configFile is: ", configFile)
  if not os.path.isfile(configFile):
    print(configFile, " is NOT a file. ") 
    with open(configFile, 'w') as out_file2:
      out_file2.write("[default]\n")
      out_file2.write(awsregion)

def deleteConfigAndCredentialsAWS():
  if platform.system() == "Windows":
    osChar = '\\'
  else:
    osChar = '/'
  #Delete files
  credFile = os.path.expanduser('~')+osChar+'.aws'+osChar+'credentials'
  print("aws credFile is: ", credFile)
  try:
    os.remove(credFile)
  except OSError:
    pass
  configFile = os.path.expanduser('~')+osChar+'.aws'+osChar+'config'
  print("aws configFile is: ", configFile)
  try:
    os.remove(configFile)
  except OSError:
    pass


def getCurrentRegion(cmd):
  print("r ----------------------------------------------------")
  logString = "About to run cli command: "+cmd
  print(logString)
  process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  logString = "data string is: " + data
  print(logString)
  logString = "err is: " + str(err)
  print(logString)
  logString = "process.returncode is: " + str(process.returncode)
  print(logString)
  if process.returncode == 0:
    logString = str(data)
    print(logString)
    print("-------")
    return data
  else:
    logString = "process.returncode is not zero.  Halting program so you can diagnose the root cause of the problem.  "
    print(logString)
    sys.exit

###############################

createConfigAndCredentialsAWS()

generatePems()

accountId = getAccount()
pushZipToS3Command = "aws s3 cp my-certs.zip s3://lf-workshop-"+accountId+"/my-certs.zip"

runCliCommand(pushZipToS3Command)

deleteFiles()

deleteConfigAndCredentialsAWS()
