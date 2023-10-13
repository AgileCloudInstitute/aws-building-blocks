import subprocess
import time
import sys

def deleteSecurityGroups(sgid, counter=0):
#  deleteSecurityGroupCmd="aws ec2 delete-security-group --group-id "+sgid
  deleteSecurityGroupCmd="ls -al"
  logString = "About to delete security group by running cli command: "+deleteSecurityGroupCmd
  print(logString)
  process = subprocess.run(deleteSecurityGroupCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    print("sgdelete return code 0")
  else:
    max = 20
    if counter < max:
      counter+=1
      logString = "INFO: The '"+deleteSecurityGroupCmd+"' command returned a non-zero return code.  Sleeping 60 seconds before retrying in case this is caused by a latency problem delaying the deletion of dependent objects. Attempt "+str(counter)+" out of "+str(max)+"."
      print(logString)
#      print("Inside deleteSecurityGroups(), vpcid is: ", vpcid)
      print("Going to try to delete security group rules in the security group one more time before sleeping and then trying to delete the security group again. ")
#      emptyOneSecurityGroup(sgid)
      time.sleep(5)
      deleteSecurityGroups(sgid, counter)
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "ERROR: The '"+deleteSecurityGroupCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)


#def deleteSecurityGroups(sgid, counter=0):
#    max = 20
#    if counter < max:
#      counter += 1
#      logString = "INFO: Attempt "+str(counter)+" out of "+str(max)+"."
#      print(logString)
#      deleteSecurityGroups(sgid, counter)

sgid = "oiuytrewq"
deleteSecurityGroups(sgid)
