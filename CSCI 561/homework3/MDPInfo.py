import collections

class MDPInfo(object):
  def __init__(self, grid, states, terminalStates, startState, disctFactor, actions, rewards, actionProbs):
    self.grid = grid
    self.states = states
    self.termStates = terminalStates
    self.start = startState
    self.gamma = disctFactor
    self.actions = actions
    self.rewards = rewards
    self.actionProbability = actionProbs

    #Create transition matrix based on mdp info
    transitionMatrix = {}
    maxRow = self.grid.shape[0] + 1
    maxCol = self.grid.shape[1] + 1
    for state in self.states:
      transitionMatrix[state] = collections.defaultdict(list)
      for action, coordMove in self.actions.iteritems():
        if 'run' in action:
          trueActionProb = float(self.actionProbability['Run'])
          unreliableProb = float(0.5 * (1.0-trueActionProb))

        elif 'walk' in action:
          trueActionProb = float(self.actionProbability['Walk'])
          unreliableProb = float(0.5 * (1.0 - trueActionProb))

        else:
          trueActionProb = None
          unreliableProb = None

        if 'Up' in action:
          if 'run' in action:
            intendedMove = (state[0] + 2, state[0])
            rightTurn = (state[0], state[1] + 2)
            leftTurn = (state[0], state[1] - 2)

          elif 'walk' in action:
            intendedMove = (state[0] + 1, state[1])
            rightTurn = (state[0], state[1] + 1)
            leftTurn = (state[0], state[1] - 1)

        elif 'Down' in action:
          if 'run' in action:
            intendedMove = (state[0] - 2, state[1])
            rightTurn = (state[0], state[1] - 2)
            leftTurn = (state[0], state[1] + 2)
          elif 'walk' in action:
            intendedMove = (state[0] -1, state[1])
            rightTurn = (state[0], state[1] - 1)
            leftTurn = (state[0], state[1] + 1)

        elif 'Left' in action:
          if 'run' in action:
            intendedMove = (state[0], state[1] - 2)
            rightTurn = (state[0] - 2, state[1])
            leftTurn = (state[0] + 2, state[1])
          elif 'walk' in action:
            intendedMove = (state[0], state[1] - 1)
            rightTurn = (state[0] - 1, state[1])
            leftTurn = (state[0] + 1, state[1])

        elif 'Right' in action:
          if 'run' in action:
            intendedMove = (state[0], state[1] + 2)
            rightTurn = (state[0] + 2, state[1])
            leftTurn = (state[0] - 2, state[1])
          elif 'walk' in action:
            intendedMove = (state[0], state[1] + 1)
            rightTurn = (state[0] + 1, state[1])
            leftTurn = (state[0] - 1, state[1])

        if (rightTurn[0] < maxRow) and (rightTurn[1] < maxCol) and (rightTurn[0] >= 0) and (rightTurn[1] >= 0):
          transitionMatrix[state][action] = (unreliableProb, rightTurn)
        if (leftTurn[0] < maxRow) and (rightTurn[1] < maxCol) and (rightTurn[0] >= 0) and (rightTurn[1] >= 0):
          transitionMatrix[state][action] = (unreliableProb, leftTurn)
        if (intendedMove[0] < maxRow) and (intendedMove[1] < maxCol) and (intendedMove[0] >= 0) and (intendedMove[1] >= 0):
          transitionMatrix[state][action] = (trueActionProb, intendedMove)
        else:
          transitionMatrix[state][action] = None


    for state in transitionMatrix.keys():
      print("\n******************************")
      print ("Current state: %s, %s" % (state[0], state[1]))
      for action in transitionMatrix[state].keys():
        print action, transitionMatrix[state][action]

    print self.grid[::-1][0][3]
    print self.grid
