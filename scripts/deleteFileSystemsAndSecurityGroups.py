
import time
import subprocess
import sys
import json


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

def getAccount(cmd='aws sts get-caller-identity'):
  logString = "About to run get account id command: "+cmd
  print(logString)
  process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
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
    logString = str(data)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "The '"+cmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def getFileSystems(cmd,account,when,counter=0):
  logString = "About to get file system ids by running cli command: "+cmd
  print(logString)
  process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    mydata = json.loads(data)
    fileSystemIds = []
    for thisfs in mydata["FileSystems"]:
      fsarn=thisfs["FileSystemArn"]
      fsowner=thisfs["OwnerId"]
      if (account in fsarn) and (fsowner==account):
        if "Tags" in thisfs:
          for fstag in thisfs["Tags"]:
            fstagkey=fstag["Key"]
            if fstagkey == "ManagedByAmazonSageMakerResource":
              fsid=thisfs["FileSystemId"]
              fileSystemIds.append(fsid)
              if when == "before":
                return fileSystemIds
              elif when == "after":
                if len(fileSystemIds) == 0:
                  return fileSystemIds
                else:
                  if counter < 5:
                    counter += 1
                    print("Sleeping 30 seconds to allow the deletions of file systems to propagate before checking their status again.")
                    time.sleep(30)
                    print("Attempt number: ", str(counter))
                    getFileSystems(fsid,when,counter)
                  else:
                    logString = "ERROR: File system still present after "+str(counter)+" retries. Stopping program so you can research the root cause of this problem. "
                    print(logString)
                    sys.exit(1)
              else:
                logString = "ERROR: Illegal value for 'when' variable in getFileSystem(): "+when+ ". Stopping program so you can research the root cause of this problem. "
                print(logString)
                sys.exit(1)
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+cmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def deleteFileSystem(fsid):
  deleteFileSystemCmd="aws efs delete-file-system --file-system-id "+fsid
  logString = "About to delete file system by running cli command: "+deleteFileSystemCmd
  print(logString)
  process = subprocess.run(deleteFileSystemCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    pass
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+deleteFileSystemCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)


def getMountTargets(fsid, when, counter=0):
  getMountTargetsCmd="aws efs describe-mount-targets --file-system-id "+fsid
  logString = "About to get mount target ids by running cli command: "+getMountTargetsCmd
  print(logString)
  process = subprocess.run(getMountTargetsCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    mydata = json.loads(data)
    mountTargetIds = []
    for thismt in mydata["MountTargets"]:
      mtid=thismt["MountTargetId"]
      mountTargetIds.append(mtid)
    if when == "before":
      return mountTargetIds
    elif when == "after":
      if len(mountTargetIds) == 0:
        return mountTargetIds
      else:
        if counter < 5:
          counter += 1
          print("Sleeping 30 seconds to allow the deletions of mount ids to propagate before checking their status again.")
          time.sleep(30)
          print("Attempt number: ", str(counter))
          getMountTargets(fsid,when,counter)
        else:
          logString = "ERROR: Mount Ids still present after "+str(counter)+" retries. Stopping program so you can research the root cause of this problem. "
          print(logString)
          sys.exit(1)
    else:
      logString = "ERROR: Illegal value for 'when' variable in getMountTargets(): "+when+ ". Stopping program so you can research the root cause of this problem. "
      print(logString)
      sys.exit(1)
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+getMountTargetsCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def deleteMountTargets(mtid):
  deleteMountTargetsCmd="aws efs delete-mount-target --mount-target-id "+mtid
  logString = "About to delete mount target by running cli command: "+deleteMountTargetsCmd
  print(logString)
  process = subprocess.run(deleteMountTargetsCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    print("mt2 return code 0")
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+deleteMountTargetsCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def revokeSecurityGroupRule(revokeCmd):
  logString = "About to revoke security group rule by running cli command: "+revokeCmd
  print(logString)
  process = subprocess.run(revokeCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    print("revoke cmd return code 0")
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+revokeCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def getSecurityGroups(vpcid, when, counter=0):
  getSecurityGroupsCmd="aws ec2 describe-security-groups"
  logString = "About to get security groups by running cli command: "+getSecurityGroupsCmd
  print(logString)
  process = subprocess.run(getSecurityGroupsCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    mydata = json.loads(data)
    securityGroupIds = []
    for thissg in mydata["SecurityGroups"]:
      if (thissg["VpcId"] == vpcid) and (("[DO NOT DELETE] Security Group" in thissg["Description"]) or ("for Elastic MapReduce created on" in thissg["Description"])):
        sgid=thissg["GroupId"]
        securityGroupIds.append(sgid)
    if when == "before":
      return securityGroupIds
    elif when == "after":
      if len(securityGroupIds) == 0:
        return securityGroupIds
      else:
        if counter < 5:
          counter += 1
          print("Sleeping 30 seconds to allow the deletions of security groups to propagate before checking their status again.")
          time.sleep(30)
          print("Attempt number: ", str(counter))
          getSecurityGroups(vpcid,when,counter)
        else:
          logString = "ERROR: Security Groups still present after "+str(counter)+" retries. Stopping program so you can research the root cause of this problem. "
          print(logString)
          sys.exit(1)
    else:
      logString = "ERROR: Illegal value for 'when' variable in getSecurityGroups(): "+when+ ". Stopping program so you can research the root cause of this problem. "
      print(logString)
      sys.exit(1)
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+getSecurityGroupsCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)

def deleteSecurityGroups(sgid):
  deleteSecurityGroupCmd="aws ec2 delete-security-group --group-id "+sgid
  logString = "About to delete security group by running cli command: "+deleteSecurityGroupCmd
  print(logString)
  process = subprocess.run(deleteSecurityGroupCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    print("sgdelete return code 0")
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+deleteSecurityGroupCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)


def getSecurityGroupRules(sgid, when, counter=0):
  getSecurityGroupRulesCmd="aws ec2 describe-security-group-rules"
  logString = "About to get security group rules by running cli command: "+getSecurityGroupRulesCmd
  print(logString)
  process = subprocess.run(getSecurityGroupRulesCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    mydata = json.loads(data)
    securityGroupRuleRevokeCmds = []
    securityGroupRuleIds = []
    for thissgr in mydata["SecurityGroupRules"]:
      if (thissgr["GroupId"] == sgid):
        sgrid=thissgr["SecurityGroupRuleId"]
        if when == "before":
          if thissgr["IsEgress"] == True:
            revokeCmd="aws ec2 revoke-security-group-egress --group-id "+sgid+" --security-group-rule-ids "+sgrid
          elif thissgr["IsEgress"] == False:
            revokeCmd="aws ec2 revoke-security-group-ingress --group-id "+sgid+" --security-group-rule-ids "+sgrid
          else:
            print("ERROR: Illegal value for IsEgress")
            sys.exit(1)
          securityGroupRuleRevokeCmds.append(revokeCmd)
        elif when == "after":
          securityGroupRuleIds.append(sgrid)
    if when == "before":
      return securityGroupRuleRevokeCmds
    elif when == "after":
      if len(securityGroupRuleIds) == 0:
        return securityGroupRuleIds
      else:
        if counter < 5:
          counter += 1
          print("Sleeping 30 seconds to allow the deletions of security group rules to propagate before checking their status again.")
          time.sleep(30)
          print("Attempt number: ", str(counter))
          getSecurityGroupRules(fsid,when,counter)
        else:
          logString = "ERROR: Security Group rules still present after "+str(counter)+" retries. Stopping program so you can research the root cause of this problem. "
          print(logString)
          sys.exit(1)
    else:
      logString = "ERROR: Illegal value for 'when' variable in getSecurityGroupRules(): "+when+ ". Stopping program so you can research the root cause of this problem. "
      print(logString)
      sys.exit(1)
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+getSecurityGroupRulesCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)


def getVPC(vname, counter=0):
  getVPCCmd='aws ec2 describe-vpcs --filters "Name=tag-value,Values='+vname+'"'
  logString = "About to get VPC by running cli command: "+getVPCCmd
  print(logString)
  process = subprocess.run(getVPCCmd, shell=True, stdout=subprocess.PIPE, text=True)
  data = process.stdout
  err = process.stderr
  if process.returncode == 0:
    mydata = json.loads(data)
    vpcIds = []
    for thisvpc in mydata["Vpcs"]:
      if (thisvpc["State"] == "available"):
        vid=thisvpc["VpcId"]
        vpcIds.append(vid)
    if len(vpcIds) >1:
      logString = "ERROR: More than one VPC contains the tag with value "+vname+". The value is intended to be unique in your account to avoid deleting unintended resources outside the intended vpc.  Halting program so you can identify the root cause of the problem. "
      print(logString)
      sys.exit(1)
    elif len(vpcIds) == 1:
      return vpcIds[0]
    else:
      if counter < 3:
        counter += 1
        print("A vpc with tag value "+vname+" was not found.  Sleeping 30 seconds before checking again in case a latency problem is causing a delay in the appearance of a matching VPC.")
        time.sleep(30)
        print("Attempt number: ", str(counter))
        getVPC(fsid,counter)
      else:
        logString = "ERROR: VPC containing tag with value "+vname+" still present after "+str(counter)+" retries. Stopping program so you can research the root cause of this problem. "
        print(logString)
        sys.exit(1)
  else:
    logString = "process.returncode is: " + str(process.returncode)
    print(logString)
    logString = "err is: " + str(err)
    print(logString)
    logString = str(data)
    print(logString)
    logString = "The '"+getVPCCmd+"' command returned a non-zero return code.  Halting program so that you can identify the root cause of the problem. "
    print(logString)
    sys.exit(1)


vpcid=getVPC("LF-Workshop-VPC")
print("vpcid is: ", vpcid)
getFsCmd="aws efs describe-file-systems"# --query 'FileSystems[*].Name' --region "+region
account=getAccount()
fileSystemIds=getFileSystems(getFsCmd,account,"before")
print("1 fileSystemIds contains: ", fileSystemIds)
if fileSystemIds:
  for fsid in fileSystemIds:
    print("a fsid is: ", fsid)
    mountTargetIds=getMountTargets(fsid, "before")
    print("a mountTargetIds contains: ", mountTargetIds)
    for mtid in mountTargetIds:
      deleteMountTargets(mtid)
  print("2 fileSystemIds contains: ", fileSystemIds)
  for fsid in fileSystemIds:
    print("b fsid is: ", fsid)
    mountTargetIds=getMountTargets(fsid, "after")
    print("b mountTargetIds contains: ", mountTargetIds)
  print("3 fileSystemIds contains: ", fileSystemIds)
  for fsid in fileSystemIds:
    print("c fsid is: ", fsid)
    deleteFileSystem(fsid)
  fileSystemIds=getFileSystems(getFsCmd,account,"after")
  print("4 fileSystemIds contains: ", fileSystemIds)



sgids=getSecurityGroups(vpcid, "before")
print("1 sgids is: ", sgids)
for sgid in sgids:
  sgrCmds = getSecurityGroupRules(sgid,"before")
  for sgrCmd in sgrCmds:
    revokeSecurityGroupRule(sgrCmd)
for sgid in sgids:
  sgrids = getSecurityGroupRules(sgid,"after")
  print("sgids for ", sgid," after deleting rules is: ", len(sgrids))
for sgid in sgids:
  deleteSecurityGroups(sgid)


