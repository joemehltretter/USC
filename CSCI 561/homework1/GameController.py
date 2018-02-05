####################################################################
#                                                                  #
# GameController.py performs the algorithms for either minimax or  #
# or alpha-beta pruning depending on the algorithm sent. It takes  #
# an initial call that initalizes a game. The other functions are  #
# the algorithms themselves.                                       #
#                                                                  #
####################################################################

from Tree import Node
import BoardConfig

class GameController(object):
  def __init__(self, player, algorithm, depth, state, pieces):
    self.player = player
    self.algorithm = algorithm
    self.maxDepth = int(depth)
    self.state = state
    self.pieces = pieces

  def Start(self):
    root = Node(self.state, None, self.player)
    currentPlayer = self.player
    maxPlayer = True
    depth = self.maxDepth
    print self.state.boardState
    if currentPlayer == 'Star':
      isStar = True
    else:
      isStar = False
    if self.algorithm == 'MINIMAX':
      score = self.Minimax(root, 0, maxPlayer, isStar)
      print("Score in start %d " % score)
      bestMove, farSightScore, numNodes  = root.TermEvaluation(score, depth, isStar)
      print bestMove, score[0], farSightScore[0], numNodes

  def Minimax(self, node, depth, maxPlayer, isStar):
    print("Entering minimax with depth of %d " % depth)
    pieces = self.pieces
    depthHolder = depth
    if depth == self.maxDepth:
      node.score = node.ScoreEvaluation()
      return node.score

    else:
      print("Getting moves")
      moves, childLocation = node.state.getMoves(isStar, pieces)
      if maxPlayer:
        score = -float("inf")
      else:
        score = float("inf")

      print("Amount of moves return %d " % len(moves))
      print("Amount of children return %d \n" % len(childLocation))
      if len(childLocation) == 0:
        print("In child location")
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
      node.score = score
      return score
        
