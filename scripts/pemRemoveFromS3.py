import datetime
import subprocess
import sys
import json
import os
import yaml
import platform

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

def find(d, tag):
    if tag in d:
        yield d[tag]

def getAcmUserHome():
    if platform.system() == 'Windows':
      acmUserHome = os.path.expanduser("~")+'/acm/'
    elif platform.system() == 'Linux':
      acmUserHome = '/usr/acm/'

    if not os.path.exists(acmUserHome):
      os.makedirs(acmUserHome, exist_ok=True) 
    return acmUserHome

def createConfigAndCredentialsAWS():
#start
  # The following assumes that you only have one set of AWS credentials in keys.yaml, and that they have the key names given below.  
  if platform.system() == "Windows":
    osChar = '\\'
  else:
    osChar = '/'
  acmUserHome = getAcmUserHome()
  keyFile = acmUserHome+osChar+'keys'+osChar+'starter'+osChar+'keys.yaml'
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
  acmConfigFile = acmUserHome+osChar+'keys'+osChar+'starter'+osChar+'config.yaml'
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

def getS3BucketName(searchTermFragment):
  cmd='aws s3api list-buckets --query "Buckets[].Name"'
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
  bucketReturnValue = ""
  if process.returncode == 0:
    mydata = json.loads(data)
    for thisBucket in mydata:
      if searchTermFragment in thisBucket:
        bucketReturnValue = thisBucket
    if bucketReturnValue != "":
      return bucketReturnValue
    else:
      logString = "ERROR: The search term '"+searchTermFragment+"' was not found in your s3 buckets.  Halting program so you can identify the root cause of this error. The bucket name is needed so that we can empty the bucket automatically before you try to delete the stack.  "
      print(logString)
      sys.exit(1)
  else:
    logString = "ERROR: The '"+cmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def emptyTheS3Bucket(bucketToEmpty):
  cmd = 'aws s3 rm s3://'+bucketToEmpty+' --recursive'
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
    return
  else:
    logString = "ERROR: The '"+cmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

###############################

createConfigAndCredentialsAWS()

accountId = getAccount()
removeZipFromS3Command = "aws s3 rm s3://lf-workshop-"+accountId+"/my-certs.zip"
runCliCommand(removeZipFromS3Command)

###############################
import datetime
print("1 str(datetime.datetime.now()) is: ", str(datetime.datetime.now()))

bucketSearchFragment = "emr-scientist-"
bucketToEmpty = getS3BucketName(bucketSearchFragment)
emptyTheS3Bucket(bucketToEmpty)

print("2 str(datetime.datetime.now()) is: ", str(datetime.datetime.now()))


deleteConfigAndCredentialsAWS()
