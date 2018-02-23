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

def main():
  #filePath = sys.argv[1]
  with open('tests/input1.txt', 'r') as openFile:
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

  #Create two neighbor variables for the constraints
  dctConfNeighbors = collections.defaultdict(list)
  dctPotNeighbors = collections.defaultdict(list)

  for country in dctVarInfo.keys():
    if dctVarInfo[country][0] == 1:
      neigh = [2,3,4]
      dctPotNeighbors[country].append(neigh)
    elif dctVarInfo[country][0] == 2:
      neigh = [1,3,4]
      dctPotNeighbors[country].append(neigh)
    elif dctVarInfo[country][0] == 3:
      neigh = [1,2,4]
      dctPotNeighbors[country].append(neigh)
    else:
      neigh = [1,2,3]
      dctPotNeighbors[country].append(neigh)
    if dctVarInfo[country][1] == 'AFC':
      neigh = ['CAF', 'OFC', 'CONCACAF', 'CONMEBOL', 'UEFA']
      dctConfNeighbors[country].append(neigh)
    elif dctVarInfo[country][1] == 'CAF':
      neigh = ['AFC', 'OFC', 'CONCACAF', 'CONMEBOL', 'UEFA']
      dctConfNeighbors[country].append(neigh)
    elif dctVarInfo[country][1] == 'OFC':
      neigh = ['AFC', 'CAF', 'CONCACAF', 'CONMEBOL', 'UEFA']
      dctConfNeighbors[country].append(neigh)
    elif dctVarInfo[country][1] == 'CONCACAF':
      neigh = ['AFC', 'CAF', 'OFC', 'CONMEBOL', 'UEFA']
      dctConfNeighbors[country].append(neigh)
    elif dctVarInfo[country][1] == 'CONMEBOL':
      neigh = ['AFC', 'CAF', 'OFC', 'CONCACAF', 'UEFA']
      dctConfNeighbors[country].append(neigh)
    else:
      neigh = ['AFC', 'CAF', 'OFC', 'CONCACAF', 'CONMEBOL']
      dctConfNeighbors[country].append(neigh)

  cspProblem = CSP.CSP(lsVariables, dctVarInfo, dctDomains, dctPotNeighbors, dctConfNeighbors, None)
  print cspProblem
  cspProblem.Solve()

if __name__ == '__main__':
  main()