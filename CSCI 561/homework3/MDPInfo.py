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
      self.stateActions[state] = collections.defaultdict(list)
      self.transitionMatrix[state] = collections.defaultdict(list)
      moves = []
      if not self.grid[::-1][state[0]][state[1]]:
        continue

      else:
        for action, coordMove in self.actions.iteritems():
          if state in self.termStates:
            moves.append('Exit')
            continue

          if 'Run' in action:
            trueActionProb = float(self.actionProbability['Run'])
            unreliableProb = float(0.5 * (1.0-trueActionProb))

          elif 'Walk' in action:
            trueActionProb = float(self.actionProbability['Walk'])
            unreliableProb = float(0.5 * (1.0 - trueActionProb))

          else:
            trueActionProb = None
            unreliableProb = None

          if 'Up' in action:
            if 'Run' in action:
              intendedMove = (state[0] + 2, state[0])
              rightTurn = (state[0], state[1] + 2)
              leftTurn = (state[0], state[1] - 2)

            if 'Walk' in action:
              intendedMove = (state[0] + 1, state[1])
              rightTurn = (state[0], state[1] + 1)
              leftTurn = (state[0], state[1] - 1)

          elif 'Down' in action:
            if 'Run' in action:
              intendedMove = (state[0] - 2, state[1])
              rightTurn = (state[0], state[1] - 2)
              leftTurn = (state[0], state[1] + 2)
            if 'Walk' in action:
              intendedMove = (state[0] -1, state[1])
              rightTurn = (state[0], state[1] - 1)
              leftTurn = (state[0], state[1] + 1)

          elif 'Left' in action:
            if 'Run' in action:
              intendedMove = (state[0], state[1] - 2)
              rightTurn = (state[0] + 2, state[1])
              leftTurn = (state[0] - 2, state[1])
            if 'Walk' in action:
              intendedMove = (state[0], state[1] - 1)
              rightTurn = (state[0] + 1, state[1])
              leftTurn = (state[0] - 1, state[1])

          elif 'Right' in action:
            if 'Run' in action:
              intendedMove = (state[0], state[1] + 2)
              rightTurn = (state[0] - 2, state[1])
              leftTurn = (state[0] + 2, state[1])
            if 'Walk' in action:
              intendedMove = (state[0], state[1] + 1)
              rightTurn = (state[0] - 1, state[1])
              leftTurn = (state[0] + 1, state[1])

          if (rightTurn[0] < maxRow) and (rightTurn[1] < maxCol) and (rightTurn[0] >= 0) and (rightTurn[1] >= 0):
            if (self.grid[::-1][rightTurn[0]][rightTurn[1]]):
              if action == 'Walk Right':
                move = 'Walk Down'
                moves.append(move)
              elif action == 'Walk Left':
                move = 'Walk Up'
                moves.append(move)
              elif action == 'Walk Up':
                move = 'Walk Right'
                moves.append(move)
              elif action == 'Walk Down':
                move = 'Walk Left'
                moves.append(move)

              if action == 'Run Right':
                move = 'Run Down'
                moves.append(move)
              elif action == 'Run Left':
                move = 'Run Up'
                moves.append(move)
              elif action == 'Run Up':
                move = 'Run Right'
                moves.append(move)
              elif action == 'Run Down':
                move = 'Run Left'
                moves.append(move)

              self.transitionMatrix[state][action].append((unreliableProb, rightTurn))
            else:
              move = 'Stay'
              moves.append(move)
              self.transitionMatrix[state][action].append((0.0, state))

          if (leftTurn[0] < maxRow) and (leftTurn[1] < maxCol) and (leftTurn[0] >= 0) and (leftTurn[1] >= 0):

            if (self.grid[::-1][leftTurn[0]][leftTurn[1]]):
              if action == 'Walk Right':
                move = 'Walk Up'
                moves.append(move)

              elif action == 'Walk Left':
                move = 'Walk Down'
                moves.append(move)
              elif action == 'Walk Up':
                move = 'Walk Left'
                moves.append(move)
              elif action == 'Walk Down':
                move = 'Walk Right'
                moves.append(move)

              if action == 'Run Right':
                move = 'Run Up'
                moves.append(move)
              elif action == 'Run Left':
                move = 'Run Down'
                moves.append(move)
              elif action == 'Run Up':
                move = 'Run Left'
                moves.append(move)
              elif action == 'Run Down':
                move = 'Run Right'
                moves.append(move)
              self.transitionMatrix[state][action].append((unreliableProb, leftTurn))
            else:
              move = 'Stay'
              moves.append(move)
              self.transitionMatrix[state][action].append((unreliableProb, state))

          if (intendedMove[0] < maxRow) and (intendedMove[1] < maxCol) and (intendedMove[0] >= 0) and (intendedMove[1] >= 0):
            if (self.grid[::-1][intendedMove[0]][intendedMove[1]]):
              moves.append(action)
              self.transitionMatrix[state][action].append((trueActionProb, intendedMove))
          else:
            moves.append('Stay')
            self.transitionMatrix[state][action].append((trueActionProb, state))
        self.stateActions[state] = moves



