###################################################################
#                                                                  #
# Starter.py is the file that will be ran to take in the input     #
# file, and parse it. It will then store variables and run the     #
# proper algorithms.                                               #
#                                                                  #
####################################################################

from GameController import GameController
from StateHandler import StateHandler
import numpy as np
import BoardConfig
import sys
import collections

def main():
  filePath = sys.argv[1]
  with open(filePath, 'r') as openFile:
    fileData = openFile.readlines()
  openFile.close()
  gameInfo = [line.strip() for line in fileData]
  currentBoard = []
  
  pieces = []
  currentPlayer = gameInfo[0]
  algToUse = gameInfo[1]
  dLimit = int(gameInfo[2])
  for line in gameInfo[3:11]:
    line = [newLine.strip() for newLine in line.split(',')]
    for obj in line:
      if obj != '0':
        pieces.append(obj)

    line = list(line)
    currentBoard.append(line)

  currentBoard = np.asarray(currentBoard)
  piecesPos = collections.defaultdict(list)
  starPos = []
  circPos = []
  for index, value in np.ndenumerate(currentBoard):
    if value in pieces:
      piecesPos[value].append(index)

  initialState = StateHandler(currentBoard, False)
  game = GameController(currentPlayer, algToUse, dLimit, initialState, pieces)
  game.Start()

if __name__=='__main__':
  main()
