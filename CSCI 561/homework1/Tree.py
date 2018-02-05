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

  def traverseTreeCount(self, children, nodesCount):
    if children is not None:
      nodesCount = nodesCount + len(children)
      for count in range(len(children)):
        nodesCount = self.traverseTreeCount(children[count].children, nodesCount)
      return nodesCount

  def traverseFarSight(self, children, farSightScore, depth):
    if children is not None:
      for count in range(len(children)):
        if children[count].depth == depth:
          score = children[count].state.getUtilityScore(self.children[count].player)
          if score > farSightScore:
            farSightScore = score
            print farSightScore
          farSightScore = self.traverseFarSight(children[count].children, farSightScore, depth)
        else:
          farSightScore = self.traverseFarSight(children[count].children, farSightScore, depth)
      return farSightScore

  def TermEvaluation(self, bestScore, depth, player):
    level = 1
    farSightScore = 0
    nodeCount = self.traverseTreeCount(self.children, level)
    farSight = self.traverseFarSight(self.children, farSightScore, depth)
    ### Get move for best score ####
    for child in self.children:
      if bestScore == child.state.getUtilityScore(player):
        bestMove = child.move.position

    return bestMove, farSight, nodeCount

    for child in self.children:
      if child.score == bestScore:
        nextMove = child.move.position
      
