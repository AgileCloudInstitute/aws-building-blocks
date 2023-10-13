import subprocess
import sys
import json

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
      logString = "ERROR: The search term '"+bucketSearchFragment+"' was not found in your s3 buckets.  Halting program so you can identify the root cause of this error. The bucket name is needed so that we can empty the bucket automatically before you try to delete the stack.  "
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
bucketSearchFragment = "emr-scientist-"
bucketToEmpty = getS3BucketName(bucketSearchFragment)
print("bucketToEmpty is: ", bucketToEmpty)
emptyTheS3Bucket(bucketToEmpty)
