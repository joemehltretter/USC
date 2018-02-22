#####################################################################
#                                                                   #
# Main file for homework assignment. This code will take an input   #
# file, parse it and store content appropriately. It will then send #
# that content to the CSP controller file.                          #
#                                                                   #
#####################################################################
import sys
import collections

def main():
  #filePath = sys.argv[1]
  with open('input1.txt', 'r') as openFile:
    fileData = openFile.readlines()
  openFile.close()
  cspInfo = [line.strip() for line in fileData]

  #Assign variables

  dNumOfGroups = int(cspInfo[0])
  dNumOfPots = int(cspInfo[1])
  dctPots = collections.defaultdict(list)
  dctConfederation = collections.defaultdict(list)
  count = 2
  intPotNum = 1
  for pot in range(dNumOfPots):
    dctPots[intPotNum] = cspInfo[count]
    count = count + 1
    intPotNum = intPotNum + 1

  for confederation in range(6):
    #parse string
    splitLine = cspInfo[count].split(':')
    strConfederation = splitLine.pop(0)
    splitLine = str(splitLine)
    splitLine = splitLine.split(',')
    count = count + 1
    for word in splitLine:
      word = word.strip('[')
      word = word.strip(']')
      word = word.strip("'")
      dctConfederation[strConfederation].append(word)


if __name__ == '__main__':
  main()