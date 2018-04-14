import copy
import collections
import numpy as np

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
    calculating = True
    while calculating:
      #Make copy of utilities and assign a delta value of 0
      # as shown in book
      dynamicUtilities = np.copy(stateUtilies)
      error = 0
      count = 0
      #Iterate and calculate new utilities values
      for state in sorted(self.mdp.states):
        count =+ 1
        toMax = []
        for action in self.mdp.actions:
          toSum = collections.defaultdict(list)
          for (probAction, stateProb) in transitions[state][action]:
            toSum[action].append(probAction * (stateProb[1] + discountFactor**count * dynamicUtilities[stateProb[0]]))
          print toSum
          toSum = {k: sum(v) for (k,v) in toSum.items()}
          print '\t', toSum
          toMax.append(sum(toSum[action]))
        print toMax
        stateUtilies[state] = max(toMax)
        #error = max(error, np.fabs(stateUtilies[state] - dynamicUtilities[state]))
      error = np.sum(np.fabs(dynamicUtilities - stateUtilies))
      if error < self.eps:
        return dynamicUtilities

  def BestPolicy(self, utilities):
    optimalPolicy = {}
    transitions = self.mdp.transitionMatrix.copy()
    for state in sorted(self.mdp.stateActions.keys()):
      if state in self.mdp.termStates:
        optimalPolicy[state] = 'Exit'
      else:
        optimalPolicy[state] = max(self.mdp.stateActions[state], key=lambda action: self.GetUpdatedUtility(action, state, utilities, transitions))
    return optimalPolicy

  def GetUpdatedUtility(self, action, state, utilities, transitions):
    updatedUtility = sum([probAction * utilities[probState[0]] for (probAction, probState) in transitions[state][action]])
    return updatedUtility