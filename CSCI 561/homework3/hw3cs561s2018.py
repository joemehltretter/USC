import DecisionMaking
import numpy as np

def main():
  testPath = 'Sample_test_cases/input2.txt'
  with open(testPath, 'r') as openFile:
    fileData = openFile.readlines()
  openFile.close()
  gridInfo = [line.strip() for line in fileData]
  count = 0

  #Grid info
  gridNums = gridInfo[count].split(',')
  gridRow = int(gridNums[0])
  gridColumn = int(gridNums[1])
  grid = np.zeros((gridRow, gridColumn))
  count = count + 1

  #Number of walls
  numOfWalls = int(gridInfo[count])

  #Walls position
  ls_wallPosition = []
  for num in range(numOfWalls):
    count = count + 1
    wallsNums = gridInfo[count].split(',')
    row = int(wallsNums[0])
    column = int(wallsNums[1])
    ls_wallPosition.append([row,column])
  count = count + 1

  #Number of terminal states
  numOfTerminalStates = int(gridInfo[count])

  #Terminal State positions
  dct_terminalStatePos = {}
  for num in range(numOfTerminalStates):
    count = count + 1
    termNums = gridInfo[count].split(',')
    row = int(termNums[0])
    column = int(termNums[1])
    weight = termNums[2]
    dct_terminalStatePos[(row, column)] = float(weight)

  #Transition model probabilities
  count = count + 1
  transitionProbs = gridInfo[count].split(',')
  dct_transitionModelProbs = {}
  dct_transitionModelProbs['flt_pWalk'] = float(transitionProbs[0])
  dct_transitionModelProbs['flt_pRun'] = float(transitionProbs[1])

  #Rewards for Rwalk and Rrun
  count = count + 1
  rewardNums = gridInfo[count].split(',')
  dct_rewardNums = {}
  dct_rewardNums['rWalk'] = float(rewardNums[0])
  dct_rewardNums['rRun'] = float(rewardNums[1])

  #Discount factor
  count = count + 1
  flt_dscntNum = float(gridInfo[count])
  print ls_wallPosition, dct_terminalStatePos, dct_transitionModelProbs, dct_rewardNums, flt_dscntNum




if __name__ == '__main__':
  main()