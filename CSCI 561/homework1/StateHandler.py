####################################################################
#                                                                  #
# StateHandler.py controls the creation and maintenance of         #
# states within the game. The code can create a state, check       #
# state of the board, check if two state of two positions, and     #
# check possible moves for a piece, and check score.               #
#                                                                  #
####################################################################
import BoardConfig
import numpy as np
import collections
from CreateMove import CreateMove

class StateHandler(object):

  def __init__(self, boardState, terminal):
    self.boardState = boardState
    self.terminal = terminal

  def createChildState(self, move, jump, currPiece, ogRow, ogCol, player):
    piecesPos = collections.defaultdict(list) 
    starPieces = []
    circlePieces = []
    if move.position == 'pass':
      boardValues = np.copy(self.boardState)
      newChild = StateHandler(boardValues, False)
      return newChild

    boardValues = np.copy(self.boardState)
    if jump:
      boardValues[jump[0]][jump[1]] = '0'
    boardValues[ogRow, ogCol] = '0'
    boardValues[move.row, move.column] = currPiece
    for index, value in np.ndenumerate(boardValues):
      if 'S' or 'C' in value:
        piecesPos[value].append(index)
    for key in piecesPos.keys():
      if 'S' in key:
        count = len(piecesPos[key])
        num = 0
        while(num < count):
          starPieces.append([piecesPos[key][num][0], piecesPos[key][num][1]])
          num += 1
      elif 'C' in key:
        count = len(piecesPos[key])
        num = 0
        while(num < count):
          circlePieces.append([piecesPos[key][num][0], piecesPos[key][num][1]])
          num += 1
    if len(circlePieces) == 0 and player == True:
      terminalState = True
    elif len(starPieces) == 0 and player == False:
      terminalState = True
    else:
      terminalState = False
    newChild = StateHandler(boardValues, terminalState)
    return newChild

  def getUtilityScore(self, player):
    score = 0
    starScore = 0
    circleScore = 0
    for index, value in np.ndenumerate(self.boardState):
      if 'S' in value:
        row1, column = np.where(self.boardState == value)
        count = int(value[1:])
        index = list(index)
        row, col = index[0], index[1]
        starScore = starScore + (BoardConfig.starScore[row] * count)
      elif 'C' in value:
        count = int(value[1:])
        index = list(index)
        row, col = index[0], index[1]
        circleScore = circleScore + (BoardConfig.circScore[row] * count)
    if player == False or player == 'Circle':
      score = circleScore - starScore
    else:
      score = starScore - circleScore
    return int(score[0])

  def checkAvailable(self, location, player):
    row, column = np.where(BoardConfig.board == location)
    piece = self.boardState[row, column]
    if piece == '0':
      return True
    elif 'S' in piece[0] and row == 0 and player == True:
      return True
    elif 'C' in piece[0] and row == 7 and player == False:
      return True
    else:
      return False

  def checkFinalRow(self, row, column, player, currPiece):
    piece = currPiece
    boardPiece = self.boardState[row, column]
    if player == True and row == 0 and 'S' in boardPiece:
      #pieceNum = int(piece[1:])
      pieceNum = int(boardPiece[1:])
      pieceNum = pieceNum + 1
      piece = 'S'+str(pieceNum)
      return piece
    elif player == False and row == 7 and 'C' in boardPiece:
      pieceNum = int(piece[1:])
      pieceNum = pieceNum + 1
      piece = 'C'+str(pieceNum)
      return piece
    else:
      return piece
 
  def checkCircleLoc(self, location, opponent, moveType):
    row, column = np.where(BoardConfig.board == location)
    for count in range(len(opponent)):
      circRow = opponent[count][0]
      circColumn = opponent[count][1]
      if row == circRow and column == circColumn:
        if moveType == 'left' and column != 0 and row != 0:
          row = row - 1
          column = column - 1
        elif moveType == 'right' and column != 7 and row != 0:
          row = row - 1
          column = column + 1
        if 'C' in self.boardState[row, column][0]:
          return False
        elif 'S' in self.boardState[row, column][0] and row == np.array([0]):
          print("True")
          return True
        else:
          return False

  def checkStarLoc(self, location, opponent, moveType):
    row, column = np.where(BoardConfig.board == location)
    for count in range(len(opponent)):
      starRow = opponent[count][0]
      starColumn = opponent[count][1]
      if row == starRow and column == starColumn:
        if moveType == 'left' and column != 0 and row != 7:
          row = row + 1
          column = column - 1
        elif moveType == 'right' and column != 7 and row != 7:
          row = row + 1
          column = column + 1
        if 'S' in self.boardState[row, column][0]:
          return False
        elif 'C' in self.boardState[row, column][0] and row == np.array([7]):
          return True
        else:
          return False

  def getMoves(self, player, pieces, endFlag):
    if endFlag:
      return [], []
    moves = []
    childStates = []
    piecesPos = collections.defaultdict(list)
    starPieces = []
    circlePieces = []
    for index, value in np.ndenumerate(self.boardState):
      if 'S' or 'C' in value:
        piecesPos[value].append(index)

    for key in piecesPos.keys():
      if 'S' in key:
        count = len(piecesPos[key])
        num = 0
        while(num < count):
          starPieces.append([piecesPos[key][num][0], piecesPos[key][num][1]])
          num += 1
      elif 'C' in key:
        count = len(piecesPos[key])
        num = 0
        while(num < count):
          circlePieces.append([piecesPos[key][num][0], piecesPos[key][num][1]])
          num += 1

    if player == True:
      for count in range(len(starPieces)):
        row = starPieces[count][0]
        column = starPieces[count][1]
        currLoc = BoardConfig.board[row, column]
        currPiece = self.boardState[row, column]
        #Check left move
        if row != 0 and column !=0:
          moveType = 'left'
          jumpLoc = None
          newRow = row - 1
          newColumn = column - 1
          newLoc = BoardConfig.board[newRow, newColumn]
          available = self.checkAvailable(newLoc, player)
          if available == True:
            pass
          elif available == False:
            isCircle = self.checkCircleLoc(newLoc, circlePieces, moveType)
            if isCircle == True:
              jumpLoc = [newRow, newColumn]
              newRow = newRow -1
              newColumn = newColumn -1
              newLoc = BoardConfig.board[newRow, newColumn]
            else:
              continue
          piece = self.checkFinalRow(newRow, newColumn, player, currPiece)
          leftMove = str(currLoc + "-" + newLoc)
          move = CreateMove(newRow, newColumn, leftMove, player)
          newChild = self.createChildState(move, jumpLoc, piece, row, column, player)
          moves.append(move)
          childStates.append(newChild)
        elif row == 0 or column == 0:
          pass

        #Check right move
        if row != 0 and column != 7:
          moveType = 'right'
          jumpLoc = None
          newRow = row - 1
          newColumn = column + 1
          newLoc = BoardConfig.board[newRow, newColumn]
          available = self.checkAvailable(newLoc, player) 
          if available == True:
            pass
          elif available == False:
            isCircle = self.checkCircleLoc(newLoc, circlePieces, moveType)
            if isCircle == True:
              jumpLoc = [newRow, newColumn]
              newRow = newRow - 1
              newColumn = newColumn + 1
              newLoc = BoardConfig.board[newRow, newColumn]
            else:
              continue
          piece = self.checkFinalRow(newRow, newColumn, player, currPiece)
          rightMove = str(currLoc + "-" + newLoc)
          move = CreateMove(newRow, newColumn, rightMove, player)
          newChild = self.createChildState(move, jumpLoc, piece, row, column, player)
          moves.append(move)
          childStates.append(newChild)
        elif row == 0 or column == 7:
          pass
      if not moves and len(starPieces) > 0:
        move = CreateMove(None, None, 'pass', player)
        newChild = self.createChildState(move, False, None, None, None, player)
        moves.append(move)
        childStates.append(newChild)
      return moves, childStates

    if player == False:
      for count in range(len(circlePieces)):
        row = circlePieces[count][0]
        column = circlePieces[count][1]
        currLoc = BoardConfig.board[row][column]
        currPiece = self.boardState[row, column]
        #Check left move
        if row != 7 and column != 7:
          moveType = 'left'
          jumpLoc = None
          newRow = row + 1
          newColumn = column + 1
          newLoc = BoardConfig.board[newRow, newColumn]
          available = self.checkAvailable(newLoc, player)
          if available == True:
            pass
          elif available == False:
            isStar = self.checkStarLoc(newLoc, starPieces, moveType)
            if isStar == True:
              jumpLoc = [newRow, newColumn]
              newRow = newRow + 1
              newColumn = newColumn - 1
              newLoc = BoardConfig.board[newRow, newColumn]
            else:
              continue
          leftMove = str(currLoc + "-" + newLoc)
          move = CreateMove(newRow, newColumn, leftMove, player)
          newChild = self.createChildState(move, jumpLoc, currPiece, row, column, player)
          moves.append(move)
          childStates.append(newChild)
        elif row == 7 or column == 0:
          pass

        #Check right move
        if row != 7 and column != 0:
          moveType = 'right'
          jumpLoc = None
          newRow = row + 1
          newColumn = column - 1
          newLoc = BoardConfig.board[newRow, newColumn]
          available = self.checkAvailable(newLoc, player)
          if available == True:
            pass
          elif available == False:
            isStar = self.checkStarLoc(newLoc, starPieces, moveType)
            if isStar == True:
              jumpLoc = [newRow, newColumn]
              newRow = row + 1
              newColumn = newColumn + 1
              newLoc = BoardConfig.board[newRow, newColumn]
            else:
              continue
          rightMove = str(currLoc + "-" + newLoc)
          move = CreateMove(newRow, newColumn, rightMove, player)
          newChild = self.createChildState(move, jumpLoc, currPiece, row, column, player)
          moves.append(move)
          childStates.append(newChild)
        elif row == 7 or column == 0:
          pass
      if not moves and len(circlePieces) > 0:
        move = CreateMove(None, None, 'pass', player)
        newChild = self.createChildState(move, False, None, None, None, player)
        moves.append(move)
        childStates.append(newChild)
      return moves, childStates
