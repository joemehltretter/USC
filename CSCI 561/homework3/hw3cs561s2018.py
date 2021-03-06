import DecisionMaking
import numpy as np
import MDPInfo as mdp

def main():
  testPath = 'Sample_test_cases/input1.txt'
  with open(testPath, 'r') as openFile:
    fileData = openFile.readlines()
  openFile.close()
  gridInfo = [line.strip() for line in fileData]
  count = 0

  #Grid info
  gridNums = gridInfo[count].split(',')
  gridRow = int(gridNums[0])
  gridColumn = int(gridNums[1])
  gridHold = np.zeros((gridRow, gridColumn), dtype=object)
  grid = gridHold[::-1]
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
    dct_terminalStatePos[(row -1, column-1)] = float(weight)

  #Transition model probabilities
  count = count + 1
  transitionProbs = gridInfo[count].split(',')
  dct_transitionProbs = {}
  dct_transitionProbs['Walk'] = float(transitionProbs[0])
  dct_transitionProbs['Run'] = float(transitionProbs[1])

  #Rewards for Rwalk and Rrun
  count = count + 1
  rewardNums = gridInfo[count].split(',')
  dct_rewardNums = {}
  dct_rewardNums['Walk'] = float(rewardNums[0])
  dct_rewardNums['Run'] = float(rewardNums[1])

  #Discount factor
  count = count + 1
  flt_dscntNum = float(gridInfo[count])

  #Create action list
  dct_actions = {'Walk Up': (1,0), 'Walk Down':(-1,0), 'Walk Right':(0,1), 'Walk Left':(0,-1), 'Run Up':(2,0),
                 'Run Down':(-2,0), 'Run Right':(0,2), 'Run Left':(0,-2)}
  ls_action = ['Walk Up', 'Walk Down', 'Walk Right', 'Walk Left', 'Run Up',
                 'Run Down', 'Run Right', 'Run Left']

  #Board Assignment
  for position in range(len(ls_wallPosition)):
    row = ls_wallPosition[position][0]
    column = ls_wallPosition[position][1]
    gridHold[row-1][column-1] = None

  for position in dct_terminalStatePos.keys():
    row = position[0]
    column = position[1]
    gridHold[row][column] = dct_terminalStatePos[position]

  #Create reward dictionary and states set for easy reference
  dct_reward = {}
  gridStates = set()

  for (row, column), value in np.ndenumerate(gridHold):
    if value == 0:
      gridHold[row][column] = -0.4

  for rowX in range(gridRow):
    for columnX in range(gridColumn):
      if gridHold[rowX][columnX]:
        gridStates.add((rowX, columnX))
        dct_reward[(rowX, columnX)] = gridHold[rowX][columnX]
  #Create Markov Decision Process object with grid info
  ls_terminalStates = list(dct_terminalStatePos.keys())
  startState = (0,0)
  mdp_Object = mdp.MDPInfo(grid, gridStates, ls_terminalStates, startState, flt_dscntNum, dct_actions, dct_reward, dct_rewardNums, dct_transitionProbs, dct_terminalStatePos)

  #Modified policy iteration for efficiency?
  #Set episolon for value iteration to identify change, set to .001 as in book
  eps = 0.0
  solver = DecisionMaking.DecisionMaking(mdp_Object, eps)
  utilities = solver.ModPolicyIteration()
  solved = solver.BestPolicy(utilities)
  for row in range(gridRow):
    for column in range(gridColumn):
      if gridHold[row][column]:
        gridHold[row][column] = solved[row,column]
      else:
        gridHold[row][column] = 'None'
  with open("output.txt", 'w') as openFile:
    count = 0
    for row in reversed(gridHold):
      if count == 0:
        openFile.write(','.join(row))
        count =+ 1
      else:
        openFile.write('\n' + ','.join(row))

if __name__ == '__main__':
  main()