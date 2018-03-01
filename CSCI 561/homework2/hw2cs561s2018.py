#####################################################################
#                                                                   #
# Main file for homework assignment. This code will take an input   #
# file, parse it and store content appropriately. It will then send #
# that content to the CSP controller file.                          #
#                                                                   #
#####################################################################
import sys
import collections
import CSP
import SearchAndCheck

def main():
  #filePath = sys.argv[1]
  with open('tests/input6.txt', 'r') as openFile:
    fileData = openFile.readlines()
  openFile.close()
  cspInfo = [line.strip() for line in fileData]

  #Assign variables

  dNumOfGroups = int(cspInfo[0])
  dNumOfPots = int(cspInfo[1])
  lsVariables = []
  dctVarInfo = collections.defaultdict(list)
  dctDomains = collections.defaultdict(list)
  count = 2
  intPotNum = 1
  for pot in range(dNumOfPots):
    splitLine = cspInfo[count].split(',')
    for country in splitLine:
      lsVariables.append(country)
      dctVarInfo[country].append(intPotNum)

      for num in range(1, dNumOfGroups+1):
        dctDomains[country].append(num)

    count = count + 1
    intPotNum = intPotNum + 1
  for confederation in range(6):
    #parse string
    splitLine = cspInfo[count].split(':')
    strConfederation = splitLine.pop(0)
    splitLine = str(splitLine)
    splitLine = splitLine.split(',')
    count = count + 1
    if 'None' not in ''.join(splitLine):
      for word in splitLine:
        word = word.strip('[')
        word = word.strip(']')
        word = word.strip("'")
        dctVarInfo[word].append(strConfederation)

  dctNeighboringCountries = collections.defaultdict(list)
  for country in dctVarInfo.keys():
    for checkCountry in lsVariables:
      if country != checkCountry:
        if dctVarInfo[country][0] == dctVarInfo[checkCountry][0]:
          if checkCountry not in dctNeighboringCountries[country]:
            dctNeighboringCountries[country].append(checkCountry)
        if dctVarInfo[country][1] == dctVarInfo[checkCountry][1]:
          if checkCountry not in dctNeighboringCountries[country]:
            dctNeighboringCountries[country].append(checkCountry)

  dctAssignments = {}
  cspProblem = CSP.CSP(lsVariables, dctVarInfo, dctDomains, dctNeighboringCountries, None)
  backtrack = SearchAndCheck.SearchAndCheck(cspProblem)
  solution = backtrack.BacktrackSearch(dctAssignments)
  if solution is not None:
    finalSolution = collections.defaultdict(list)
    for country, group in solution.iteritems():
      finalSolution[group].append(country)
    print("Yes")
    for group in finalSolution.keys():
      countries = str(finalSolution[group]).replace(']', '')
      countries = countries.replace('[', '')
      countries = countries.replace("'", '')
      print countries
  else:
    print("No")

if __name__ == '__main__':
  main()