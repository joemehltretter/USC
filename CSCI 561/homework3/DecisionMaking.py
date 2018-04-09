import copy
import numpy as np
class DecisionMaking(object):
  def __init__(self, mdpobject, eps):
    self.mdp = mdpobject
    self.board = copy.deepcopy(mdpobject.grid[::-1])
    self.grid = self.board[::-1]
    self.eps = eps

  def ModPolicyIteration(self):
    #Assign default utility values
    stateUtilies = {state: 0 for state in self.mdp.states}
    rewards = self.mdp.rewards
    transitions = self.mdp.transitionMatrix
    discountFactor = self.mdp.gamma
    calculating = True
    while calculating:
      #Make copy of utilities and assign a delta value of 0
      # as shown in book
      dynamicUtilities = stateUtilies.copy()
      error = 0

      #Iterate and calculate new utilities values
      for state in self.mdp.stateActions.keys():
        stateUtilies[state] = rewards[state] + discountFactor * max(sum(probAction*dynamicUtilities[stateProb] for (probAction, stateProb) in transitions[state][action])
                                                    for action in self.mdp.stateActions[state])
        error = max(error, abs(stateUtilies[state] - dynamicUtilities[state]))
      if error < self.eps * (1 - discountFactor)/discountFactor:
        return dynamicUtilities

  def BestPolicy(self, utilities):
    optimalPolicy = {}
    transitions = self.mdp.transitionMatrix
    for state in self.mdp.stateActions.keys():
      optimalPolicy[state] = max(self.mdp.stateActions[state], key=lambda action: self.GetUpdatedUtility(action, state, utilities, transitions))
    return optimalPolicy

  def GetUpdatedUtility(self, action, state, utilities, transitions):
    updatedUtility = sum(probAction * utilities[probState] for (probAction, probState) in transitions[state][action])
    print updatedUtility
    return updatedUtility