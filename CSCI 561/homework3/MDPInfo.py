import collections

class MDPInfo(object):
  def __init__(self, grid, states, terminalStates, startState, disctFactor, actions, rewards, actionProbs):
    self.grid = grid
    self.states = states
    self.termStates = terminalStates
    self.start = startState
    self.gamma = disctFactor
    self.actions = actions
    self.stateActions = {}
    self.rewards = rewards
    self.actionProbability = actionProbs

    #Create transition matrix based on mdp info
    self.transitionMatrix = {}
    maxRow = self.grid.shape[0]
    maxCol = self.grid.shape[1]
    for state in self.states:
      if not self.grid[::-1][state[0]][state[1]]:
        continue

      else:
        self.stateActions[state] = collections.defaultdict(list)
        self.transitionMatrix[state] = collections.defaultdict(list)
        moves = []
        transitions = []
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

            if (self.grid[::-1][rightTurn[0]][rightTurn[1]]):

              if 'walk' in action:
                move = 'walk_Right'
                moves.append(move)

              if 'run' in action:
                move = 'run_Right'
                moves.append(move)
              self.transitionMatrix[state][action].append((unreliableProb, rightTurn))

          if (leftTurn[0] < maxRow) and (leftTurn[1] < maxCol) and (leftTurn[0] >= 0) and (leftTurn[1] >= 0):

            if (self.grid[::-1][leftTurn[0]][leftTurn[1]]):

              if 'walk' in action:
                move = 'walk_Left'
                moves.append(move)

              if 'run' in action:
                move = 'run_Left'
                moves.append(move)
              self.transitionMatrix[state][action].append((unreliableProb, leftTurn))

          if (intendedMove[0] < maxRow) and (intendedMove[1] < maxCol) and (intendedMove[0] >= 0) and (intendedMove[1] >= 0):
            if (self.grid[::-1][intendedMove[0]][intendedMove[1]]):
              moves.append(action)
              self.transitionMatrix[state][action].append((trueActionProb, intendedMove))
        self.stateActions[state] = moves
    #print self.grid[::-1][self.termStates[0][0]][self.termStates[0][1]]
    #print self.grid[::-1][0][3]




