import subprocess
import sys
import json
import time
import os
import yaml
import platform

inputArgs=sys.argv
 
def getCrawlerStatus(cmd,counter=0):
  if counter == 0:
    print("Sleeping 15 seconds before checking the crawler's status the first time to make sure the crawler has time to start running first. ")
    time.sleep(15)
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
    print("type(mydata) is: ", type(mydata))
    myState = mydata["Crawler"]["State"]
    print("Crawler State is: ", myState)
    if myState == "READY":
      myLastCrawl = mydata["Crawler"]["LastCrawl"]
      myLastCrawlStatus = mydata["Crawler"]["LastCrawl"]["Status"]
      print("myLastCrawl is: ", str(myLastCrawl))
      print("myLastCrawlStatus is: ", str(myLastCrawlStatus))
      if myLastCrawlStatus == "SUCCEEDED":
        print("Crawler run succeeded.  ")
        return
      else:
        if 'ErrorMessage' in myLastCrawl:
          myLastCrawl["ErrorMessage"]
          print('myLastCrawl["ErrorMessage"] is: ', myLastCrawl["ErrorMessage"])
        else:
          print("No error message reported.")
        print("Crawler run did NOT succeed.  Halting program so that you can examine the root cause of the problem. ")
        sys.exit(1)
    elif  (myState == "RUNNING") or (myState == "STOPPING"):
      if counter < 31:
        logString = "Crawler is "+myState+".  Sleeping 30 seconds before checking its state again. "
        print(logString)
        counter +=1 
        logString = "Attempt "+str(counter)+ " out of 30. "
        print(logString)
        time.sleep(30)
        getCrawlerStatus(cmd,counter)
    else: 
      logString = "An unexpected value ( "+str(myState)+" ) was returned for the crawler's State. Halting program so you can identify the root cause.  "
      print(logString)
      sys.exit(1)
  else:
    if counter < 31:
      logString = "The 'aws glue get-crawler' command returned a non-zero return code.  Sleeping 30 seconds before running the command another time in case a latency problem or a connectivity problem caused the attempt to fail. "
      print(logString)
      counter +=1 
      logString = "Attempt "+str(counter)+ " out of 30. "
      print(logString)
      time.sleep(30)
      getCrawlerStatus(cmd,counter)
    else:
      exitFunction(err, process)

def exitFunction(err, process):
  logString = "Error: " + str(err)
  print(logString)
  logString = "Error: Return Code is: " + str(process.returncode)
  print(logString)
  logString = "ERROR: Failed to return Json response.  Halting the program so that you can debug the cause of the problem."
  print(logString)
  sys.exit(1)

def startCrawler(cmd, myName):
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
  getCmd = 'aws glue get-crawler --name "'+myName+'"'
  getCrawlerStatus(getCmd)
#  getCrawlerStatus('aws glue get-crawler --name "TPC Crawler"')

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

#The following function will set all the values for the returned properties
def processInputArgs(inputArgs):
    print("y")
    print("str(inputArgs) is: ", inputArgs)
    if (inputArgs[1].startswith('name=')):
      name = (inputArgs[1])[5:]
      print("name is: ", name)
    else:
      logString = "ERROR: Illegal syntax.  Command must look like 'python crawlerController.py name=nameOfCrawler'.  "
      print(logString)
      sys.exit(1)
    return name

createConfigAndCredentialsAWS()

myregion = getCurrentRegion("aws configure get region")
myName = processInputArgs(inputArgs)
myCmd = 'aws glue start-crawler --name "'+myName+'"' +' --region '+myregion
print("myCmd is: ", myCmd)

startCrawler(myCmd, myName)

print("Finished running crawler.  Going to sleep 2 minutes to allow the resource creations ot propagate before continuing on to downstream processes that require them. ")
time.sleep(120)

deleteConfigAndCredentialsAWS()

#python crawlerController.py name="TPC Crawler"

