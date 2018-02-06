####################################################################
#                                                                  #
# GameController.py performs the algorithms for either minimax or  #
# or alpha-beta pruning depending on the algorithm sent. It takes  #
# an initial call that initalizes a game. The other functions are  #
# the algorithms themselves.                                       #
#                                                                  #
####################################################################

from Tree import Node, ABNode
import BoardConfig

class GameController(object):
  def __init__(self, player, algorithm, depth, state, pieces):
    self.player = player
    self.algorithm = algorithm
    self.maxDepth = int(depth)
    self.state = state
    self.pieces = pieces

  def Start(self):
    currentPlayer = self.player
    maxPlayer = True
    depth = self.maxDepth
    print self.state.boardState
    if currentPlayer == 'Star':
      isStar = True
    else:
      isStar = False
    if self.algorithm == 'MINIMAX':
      root = Node(self.state, None, self.player)
      score = self.Minimax(root, 0, maxPlayer, isStar)
      bestMove, score, farSightScore, numNodes  = root.TermEvaluation(score, depth, isStar)
      print bestMove, score, farSightScore, numNodes
      with open('output.txt', 'w') as openFile:
        openFile.write(bestMove +'\n')
        openFile.write(str(score) + '\n')
        openFile.write(str(farSightScore) + '\n')
        openFile.write(str(numNodes))
 
    elif self.algorithm == 'ALPHABETA':
      root = ABNode(self.state, None, self.player)
      alpha = -float("inf")
      beta = float("inf")
      score = self.AlphaBeta(root, 0, maxPlayer, isStar, alpha, beta)
      bestMove, score, farSightScore, numNodes = root.TermEvaluation(score, self.maxDepth, isStar)
      print bestMove, score, farSightScore, numNodes 

  def AlphaBeta(self, node, depth, maxPlayer, isStar, alpha, beta):
    pieces = self.pieces
    if depth == self.maxDepth:
      node.score = node.ScoreEvaluation()
      return node.score
    else:
      endFlag = node.checkEnd()
      moves, childLocation = node.state.getMoves(isStar, pieces, endFlag)
      if endFlag:
        self.maxDepth = depth

      if len(childLocation) == 0:
        node.score = node.ScoreEvaluation()
        return node.score
      for index in range(len(childLocation)):
        childState, move = childLocation[index], moves[index]
        childNode = ABNode(childState, move, isStar)
        node.addChild(childNode)
        childScore = self.AlphaBeta(childNode, depth+1, not maxPlayer, not isStar, alpha, beta)
        if maxPlayer:
          alpha = max(alpha, childScore)
          node.score = alpha
          if beta <= alpha:
            return alpha
        else:
          beta = min(beta, childScore)
          node.score = beta
          if beta <= alpha:
            return beta

      node.alpha = alpha
      node.beta = beta
      if maxPlayer:
        return alpha
      else:
        return beta

  def Minimax(self, node, depth, maxPlayer, isStar):
    pieces = self.pieces

    if depth == self.maxDepth:
      node.score = node.ScoreEvaluation()
      return node.score

    else:
      endFlag = node.checkEnd()
      moves, childLocation = node.state.getMoves(isStar, pieces, endFlag)
      if maxPlayer:
        score = -float("inf")
      else:
        score = float("inf")

      if len(childLocation) == 0:
        node.score = node.ScoreEvaluation()
        return node.score
      for index in range(len(childLocation)):
        childState, move = childLocation[index], moves[index]
        childNode = Node(childState, move, isStar)
        node.addChild(childNode)
        childScore = self.Minimax(childNode, depth+1, not maxPlayer, not isStar) 
        if maxPlayer:
          score = max(score, childScore)
        else:
          score = min(score, childScore)
      #node.score = score
      return score
        
