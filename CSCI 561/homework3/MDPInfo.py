import collections

class MDPInfo(object):
  def __init__(self, grid, states, terminalStates, startState, disctFactor, actions, testRew, rewardNums, actionProbs, termRewards):
    self.grid = grid
    self.states = states
    self.termStates = terminalStates
    self.start = startState
    self.gamma = disctFactor
    self.actions = actions
    self.stateActions = {}
    self.rewardNums = rewardNums
    self.rewards = {}
    self.rewardsTest = testRew
    self.actionProbability = actionProbs
    self.termRewards = termRewards

    #Create transition matrix based on mdp info
    self.transitionMatrix = {}
    self.maxRow = len(self.grid)-1
    self.maxCol = len(self.grid[0])-1
    for state in sorted(self.states):
      self.stateActions[state] = collections.defaultdict(list)
      self.transitionMatrix[state] = collections.defaultdict(list)
      self.rewards[state] = collections.defaultdict(list)
      moves = []
      if not self.grid[::-1][state[0]][state[1]]:
        continue

      else:
        for action, coordMove in self.actions.iteritems():
          if 'Run' in action:
            intededProb = float(self.actionProbability['Run'])
            unintendedProb = float(0.5*(1.0-intededProb))
          elif 'Walk' in action:
            intededProb = float(self.actionProbability['Walk'])
            unintendedProb = float(0.5 * (1.0 - intededProb))
          self.transitionMatrix[state][action] = self.GetTransitions(state, action, intededProb, unintendedProb)

  def GetTransitions(self, state, action, intendProb, unintendProb):
    if state in self.termStates:
      reward = self.termRewards[state]
      return [(intendProb, (state, reward)),
              (unintendProb, (state, reward)),
              (unintendProb, (state, reward))]
    else:
      if 'Run' in action:
        return [(intendProb, self.makeIntendedRunMove(state, action)),
                (unintendProb, self.makeUnintendedRunRight(state, action)),
                (unintendProb, self.makeUnintendedRunLeft(state, action))]
      elif 'Walk' in action:
        return [(intendProb, self.makeIntendedWalkMove(state, action)),
                (unintendProb, self.makeUnintendedWalkRight(state, action)),
                (unintendProb, self.makeUnintendedWalkLeft(state, action))]

  def makeIntendedRunMove(self, state, action):
    reward = self.rewardNums['Run']
    if 'Up' in action and state[0] + 2 <= self.maxRow:
      if self.grid[::-1][state[0] + 2][state[1]] and self.grid[::-1][state[0]+1][state[1]]:
        if (state[0]+2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+2, state[1])]
        return ((state[0]+2, state[1]), reward)
      else:
        return (state, reward)
    elif 'Down' in action and state[0] - 2 >= 0:
      if self.grid[::-1][state[0] - 2][state[1]] and self.grid[::-1][state[0]-1][state[1]]:
        if (state[0]-2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-2, state[1])]
        return ((state[0] - 2, state[1]), reward)
      else:
        return (state, reward)
    elif 'Right' in action and ((state[1] + 2) <= self.maxCol):
      if self.grid[::-1][state[0]][state[1]+2] and self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+2)]
        return ((state[0], state[1]+2), reward)
      else:
        return (state, reward)
    elif 'Left' in action and state[1] - 2 >= 0:
      if self.grid[::-1][state[0]][state[1]-2] and self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1] - 2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]-2)]
        return ((state[0], state[1]-2), reward)
      else:
        return (state, reward)
    else:
      return (state, reward)

  def makeIntendedWalkMove(self, state, action):
    reward = self.rewardNums['Walk']
    if 'Up' in action and state[0] + 1 <= self.maxRow:
      if self.grid[::-1][state[0] + 1][state[1]]:
        if (state[0]+1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+1, state[1])]
        self.stateActions[state][action].append('Walk Up')
        return ((state[0] + 1, state[1]), reward)
      else:
        self.stateActions[state][action].append('Walk Up')
        return ((state[0], state[1]), reward)
    elif 'Down' in action and state[0] - 1 >= 0:
      if self.grid[::-1][state[0] - 1][state[1]]:
        if (state[0]-1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-1, state[1])]
        self.stateActions[state][action].append('Walk Down')
        return ((state[0] - 1, state[1]), reward)
      else:
        return ((state[0], state[1]), reward)
    elif 'Right' in action and state[1] + 1 <= self.maxCol:
      if self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+1) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+1)]
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]+1), reward)
      else:
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]), reward)
    elif 'Left' in action and state[1] - 1 >= 0:
      if self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1]-1) in self.termStates:
          reward = self.termRewards[(state[0], state[1]-1)]
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]-1), reward)
      else:
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]), reward)
    else:
      return ((state[0], state[1]), reward)
  def makeUnintendedRunRight(self, state, action):
    reward = self.rewardNums['Run']
    if 'Up' in action and state[1] + 2 <= self.maxCol:
      if self.grid[::-1][state[0]][state[1]+2] and self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+2)]
        self.stateActions[state][action].append('Run Right')
        return ((state[0], state[1]+2), reward)
      else:
        self.stateActions[state][action].append('Run Right')
        return ((state[0], state[1]), reward)
    elif 'Down' in action and state[1] -2 >= 0:
      if self.grid[::-1][state[0]][state[1]-2] and self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1]-2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]-2)]
        self.stateActions[state][action].append('Run Left')
        return ((state[0], state[1]-2), reward)
      else:
        self.stateActions[state][action].append('Run Left')
        return ((state[0], state[1]), reward)
    elif 'Right' in action and state[0] - 2 >= 0:
      if self.grid[::-1][state[0]-2][state[1]] and self.grid[::-1][state[0]-1][state[1]]:
        if (state[0]-2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-2, state[1])]
        self.stateActions[state][action].append('Run Down')
        return ((state[0]-2, state[1]), reward)
      else:
        self.stateActions[state][action].append('Run Down')
        return ((state[0], state[1]), reward)
    elif 'Left' in action and state[0] + 2 <= self.maxRow:
      if self.grid[::-1][state[0]+2][state[1]] and self.grid[::-1][state[0]+1][state[1]]:
        if (state[0]+2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+2, state[1])]
        self.stateActions[state][action].append('Run Up')
        return ((state[0]+2, state[1]), reward)
      else:
        self.stateActions[state][action].append('Run Up')
        return ((state[0], state[1]), reward)
    else:
      return ((state[0], state[1]), reward)
  def makeUnintendedWalkRight(self, state, action):
    reward = self.rewardNums['Walk']
    if 'Up' in action and state[1] + 1 <= self.maxCol:
      if self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+1) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+1)]
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]+1), reward)
      else:
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]), reward)
    elif 'Down' in action and state[1] - 1 >= 0:
      if self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1]-1) in self.termStates:
          reward = self.termRewards[(state[0], state[1]-1)]
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]-1), reward)
      else:
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]), reward)
    elif 'Right' in action and state[0] -1 >= 0:
      if self.grid[::-1][state[0]-1][state[1]]:
        if (state[0]-1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-1, state[1])]
        self.stateActions[state][action].append('Walk Down')
        return ((state[0]-1, state[1]), reward)
      else:
        self.stateActions[state][action].append('Walk Down')
        return ((state[0], state[1]), reward)
    elif 'Left' in action and state[0] + 1 <= self.maxRow:
      if self.grid[::-1][state[0]+1][state[1]]:
        if (state[0]+1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+1, state[1])]
        self.stateActions[state][action].append('Walk Up')
        return ((state[0]+1, state[1]), reward)
      else:
        self.stateActions[state][action].append('Walk Up')
        return ((state[0], state[1]), reward)
    else:
      return ((state[0], state[1]), reward)
  def makeUnintendedRunLeft(self, state, action):
    reward = self.rewardNums['Run']
    if 'Up' in action and state[1] - 2 >= 0:
      if self.grid[::-1][state[0]][state[1]-2] and self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1]-2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]-2)]
        self.stateActions[state][action].append('Run Left')
        return ((state[0], state[1]-2), reward)
      else:
        self.stateActions[state][action].append('Run Left')
        return ((state[0], state[1]), reward)
    elif 'Down' in action and state[1] + 2 <= self.maxCol:
      if self.grid[::-1][state[0]][state[1]+2] and self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+2) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+2)]
        self.stateActions[state][action].append('Run Right')
        return ((state[0], state[1]+2), reward)
      else:
        self.stateActions[state][action].append('Run Right')
        return ((state[0], state[1]), reward)
    elif 'Right' in action and state[0] + 2 <= self.maxRow:
      if self.grid[::-1][state[0]+2][state[1]] and self.grid[::-1][state[0]+1][state[1]]:
        if (state[0]+2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+2, state[1])]
        self.stateActions[state][action].append('Run Up')
        return ((state[0]+2, state[1]), reward)
      else:
        self.stateActions[state][action].append('Run Up')
        return ((state[0], state[1]),reward)
    elif 'Left' in action and state[0] - 2 >= 0:
      if self.grid[::-1][state[0]-2][state[1]] and self.grid[::-1][state[0]-1][state[1]]:
        if (state[0]-2, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-2, state[1])]
        self.stateActions[state][action].append('Run Down')
        return ((state[0]-2, state[1]), reward)
      else:
        self.stateActions[state][action].append('Run Down')
        return ((state[0], state[1]), reward)
    else:
      return ((state[0], state[1]), reward)
  def makeUnintendedWalkLeft(self,state, action):
    reward = self.rewardNums['Walk']
    if 'Up' in action and state[1] - 1 >= 0:
      if self.grid[::-1][state[0]][state[1]-1]:
        if (state[0], state[1]-1) in self.termStates:
          reward = self.termRewards[state[0], state[1]-1]
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]-1), reward)
      else:
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]), reward)
    elif 'Down' in action and state[1] + 1 <= self.maxCol:
      if self.grid[::-1][state[0]][state[1]+1]:
        if (state[0], state[1]+1) in self.termStates:
          reward = self.termRewards[(state[0], state[1]+1)]
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]+1), reward)
      else:
        self.stateActions[state][action].append('Walk Right')
        return ((state[0], state[1]), reward)
    elif 'Right' in action and state[0] + 1 <= self.maxRow:
      if self.grid[::-1][state[0]+1][state[1]]:
        if (state[0] + 1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]+1, state[1])]
        self.stateActions[state][action].append('Walk Up')
        return ((state[0]+1,state[1]), reward)
      else:
        self.stateActions[state][action].append('Walk Up')
        return ((state[0], state[1]), reward)
    elif 'Left' in action and state[0] - 1 >= 0:
      if self.grid[::-1][state[0]-1][state[1]]:
        if (state[0]-1, state[1]) in self.termStates:
          reward = self.termRewards[(state[0]-1, state[1])]
        self.stateActions[state][action].append('Walk Down')
        return ((state[0]-1, state[1]), reward)
      else:
        self.stateActions[state][action].append('Walk Left')
        return ((state[0], state[1]), reward)
    else:
      return ((state[0], state[1]), reward)

