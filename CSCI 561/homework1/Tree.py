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

  def traverseScore(self, children, farSightScore, depth, player, lock):
    if children is not None:
      for count in range(len(children)):
        score = children[count].state.getUtilityScore(player)
        if children[count].depth == depth and lock is False:
          if score > farSightScore:
            farSightScore = score
          farSightScore = self.traverseScore(children[count].children, farSightScore, depth, player, lock)
        elif children[count].state.terminal == True:
          lock = True
          if score > farSightScore:
            farSightScore = score
          farSightScore = self.traverseScore(children[count].children, farSightScore, depth, player, lock)
        else:
          farSightScore = self.traverseScore(children[count].children, farSightScore, depth, player, lock)
      return farSightScore

  def traverseUtilityScore(self, children, utilityScore, depth, player):
    if children is not None:
      for count in range(len(children)):
        if children[count].depth == 1:
          uScore = children[count].state.getUtilityScore(player)
          if uScore > utilityScore:
            utilityScore = max(utilityScore, uScore)
          utilityScore = self.traverseUtilityScore(children[count].children, utilityScore, depth, player)
      return utilityScore

  def TermEvaluation(self, bestScore, depth, player):
    level = 1
    farSightScore = 0
    utilityScore = 0
    nodeCount = self.traverseTreeCount(self.children, level)
    print self.player
    farSight = self.traverseScore(self.children, farSightScore, depth, self.player, False)
    utilityScore = self.traverseUtilityScore(self.children, utilityScore, depth, self.player)
    print farSight, utilityScore
    ### Get move for best score ####
    for child in self.children:
      if utilityScore == child.state.getUtilityScore(player):
        bestMove = child.move.position

    return bestMove, utilityScore, farSight, nodeCount

    for child in self.children:
      if child.score == bestScore:
        nextMove = child.move.position
      
