import copy
import collections
import numpy as np
import operator

class DecisionMaking(object):
  def __init__(self, mdpobject, eps):
    self.mdp = mdpobject
    self.board = copy.deepcopy(mdpobject.grid[::-1])
    self.grid = self.board[::-1]
    self.eps = eps

  def ModPolicyIteration(self):
    #Assign default utility values
    #stateUtilies = {state: 0.0 for state in self.mdp.states}
    stateUtilies = np.zeros(self.mdp.grid.shape)
    transitions = self.mdp.transitionMatrix
    discountFactor = self.mdp.gamma
    maxIterations = 10000
    calculating = True
    for iteration in range(maxIterations):
      #Make copy of utilities and assign a delta value of 0
      # as shown in book
      dynamicUtilities = np.copy(stateUtilies)
      error = 1
      count = 0
      #Iterate and calculate new utilities values
      for state in sorted(self.mdp.states):
        if state in self.mdp.termStates:
          maxToBeat = [self.mdp.termRewards[state]]
        else:
          count =+ 1
          toMax = collections.defaultdict(list)
          for action in self.mdp.actions:
            if state in self.mdp.termStates:
              rew = self.mdp.termRewards[state]
              stateUtilies[state] = rew
            elif 'Walk' in action:
              rew = self.mdp.rewardNums['Walk']
            elif 'Run' in action:
              rew = self.mdp.rewardNums['Run']
            toSum = collections.defaultdict(list)
            for (probAction, stateProb) in transitions[state][action]:
              toSum[action].append(probAction * (rew + discountFactor**count * dynamicUtilities[stateProb[0]]))
            toSum = {k: sum(v) for (k,v) in toSum.items()}
            toMax[action].append(toSum[action])
          maxCount = 0
          for maxAction in toMax.keys():
            if maxCount == 0:
              currentMax = maxAction
              maxToBeat = toMax[maxAction]
              maxCount =+ 1
            else:
              if toMax[maxAction] > maxToBeat:
                maxToBeat = toMax[maxAction]
                currentMax = maxAction
              elif toMax[maxAction] == maxToBeat:
                currentMax = self.BreakTie(currentMax, maxAction)
                maxToBeat = toMax[currentMax]

        stateUtilies[state] = maxToBeat[0]
        #error = max(error, np.fabs(stateUtilies[state] - dynamicUtilities[state]))
      error = np.sum(np.fabs(dynamicUtilities - stateUtilies))
      if error == self.eps:
        return stateUtilies

  def BreakTie(self, current, new):
    tieBreakerList = ['Walk Up', 'Walk Down', 'Walk Left', 'Walk Right', 'Run Up', 'Run Down', 'Run Left', 'Run Right']
    currentNum = tieBreakerList.index(current)
    newNum = tieBreakerList.index(new)
    if currentNum < newNum:
      return current
    else:
      return new
  def BestPolicy(self, utilities):
    optimalPolicy = {}
    transitions = self.mdp.transitionMatrix.copy()
    discountCount = 0
    for state in sorted(self.mdp.states):
      discountCount =+ 1
      toMax = collections.defaultdict(list)
      if state in self.mdp.termStates:
        optimalPolicy[state] = 'Exit'
      else:
        #for state in sorted(self.mdp.states):
        for action in self.mdp.actions.keys():
          toSum = collections.defaultdict(list)
          toSum[action].append(self.GetUpdatedUtility(action, state, utilities, transitions, discountCount))
          toMax[action].append(toSum[action])

        maxCount = 0
        for maxAction in toMax.keys():
          if maxCount == 0:
            currentMax = maxAction
            maxToBeat = toMax[maxAction]
            maxCount = + 1
          else:
            if round(toMax[maxAction][0][0],10) > round(maxToBeat[0][0],10):
              maxToBeat = toMax[maxAction]
              currentMax = maxAction
            elif round(toMax[maxAction][0][0],10) == round(maxToBeat[0][0],10):
              currentMax = self.BreakTie(currentMax, maxAction)
              maxToBeat = toMax[currentMax]
            elif toMax[maxAction] < maxToBeat:
              pass
        optimalPolicy[state] = currentMax
        #optimalPolicy[state] = max(self.mdp.stateActions[state], key=lambda action: self.GetUpdatedUtility(action, state, utilities, transitions))
    return optimalPolicy

  def GetUpdatedUtility(self, action, state, utilities, transitions, count):
    if 'Run' in action:
      rew = self.mdp.rewardNums['Run']
    elif 'Walk' in action:
      rew = self.mdp.rewardNums['Walk']
    updatedUtility = sum([probAction *(rew + self.mdp.gamma**count * utilities[probState[0]]) for (probAction, probState) in transitions[state][action]])
    return updatedUtility