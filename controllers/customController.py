
import sys
import os

inputArgs=sys.argv
templateFile = ''

print("Inside Custom Controller! ")
print("len(inputArgs) is: ", len(inputArgs))
#First process the domain and the command
if len(inputArgs) > 1:
  for thisArg in inputArgs:
    print("thisArg is: ", thisArg)
    if thisArg.replace(" ", "").startswith("--templateFile://"):
      templateFile = thisArg.replace(" ","").replace('--templateFile://','')
print('templateFile is: ', templateFile)
if not os.path.exists(templateFile):
  logString = "ERROR in customController. templateFile is not an actual file: "+str(templateFile)
  quit(logString)

#Uncomment the next line to test throwing an error from the customController.
#quit('Error in custom controller')

print('inputArgs[0] is: ', inputArgs[0])
print('inputArgs[1] is: ', inputArgs[1])
print('inputArgs[2] is: ', inputArgs[2])

#FOR TESTING ONLY: hard-coding output variables so you can see working example of format for output.  Your actual custom controller would need code to interpolate the values of output variables from whatever source system you are controlling.
outputVars = [
{'varName':'firstOutputVar', 'varValue':'value-for-first-output-variable'},
{'varName':'secondOutputVar', 'varValue':'value-for-second-output-variable'}
]

if len(outputVars) > 0:
  print('Output variables:')
  for outputVariable in outputVars:
    print(outputVariable['varName'], ' = ', outputVariable['varValue'])
  print('Finished output variables.')
print('About to exit custom controller.')
exit(1)
