import copy

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
        uToSum = []
        for action in self.mdp.stateActions[state]:
          if transitions[state][action]:
            print type(transitions[state][action]), transitions[state][action]
            for prob, new in transitions[state][action]:
              print prob, new
        #stateUtilies[state] = rewards[state] + discountFactor * max(sum(uToSum))

        #stateUtilies[state] = rewards[state] + discountFactor * max(sum(probAction*dynamicUtilities[state] (probAction, probState) = transitions[state][action])
        #                                            for action in self.mdp.stateActions[state])
        #print stateUtilies[state], rewards[state], discountFactor
        #error = max(error, abs(stateUtilies[state] - dynamicUtilities[state]))

      if error < self.eps * (1 - discountFactor)/discountFactor:
        return dynamicUtilities

    #print self.board
    #print self.board[0][3]