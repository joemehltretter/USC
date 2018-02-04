####################################################################
#                                                                  #
#  Tree.py controlls the tree for the game being played. It takes  #
#  an input and creates an intiailization for the tree. It then    #
#  can add children to the instance.                               #
#                                                                  #
####################################################################
import BoardConfig

class Node(object):
  def __init__(self, state, move, player):
    self.state = state
    self.children = []
    self.depth = 0
    self.parent = None
    self.move = move
    self.player = player
    self.farsightedScore = 0

  def ScoreEvaluation(self):
    return self.state.getUtilityScore(self.player)

  def addChild(self, childNode):
    self.children.append(childNode)
    childNode.parent = self
    childNode.depth = self.depth + 1

  def TermEvaluation(self, bestScore, depth, player):
    level = 1
    farSightScore = 0
    ### Get move for best score ####
    for child in self.children:
      if bestScore == child.state.getUtilityScore(player):
        bestMove = child.move.position

    for treeLevel in range(depth):
      level = level + 1
      if self.children[treeLevel]:
        if len(self.children[treeLevel].children) > 0:
          for count in range(len(self.children[treeLevel].children)):
            level = level + 1
            if((treeLevel + 1) == depth):
              currScore = self.children[treeLevel].children[count].state.getUtilityScore(player)
              if currScore > farSightScore:
                farSightScore = currScore
    return bestMove, farSightScore, level

    for child in self.children:
      if child.score == bestScore:
        nextMove = child.move.position
      
