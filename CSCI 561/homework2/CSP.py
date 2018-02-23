#####################################################################
#                                                                   #
# CSP.py will be the file that does all the CSP work to solve the   #
# problem.                                                          #
#                                                                   #
#####################################################################
import collections

class CSP(object):
  def __init__(self, variables, variableInfo, domains, potNeighbors, confNeighbors, constraints):
    self.variables = variables
    self.valInfo = variableInfo
    self.domains = domains
    self.potNeighbors = potNeighbors
    self.confNeighbors = confNeighbors
    self.constraints = constraints
    self.assignments = collections.defaultdict(list)

  def Solve(self):
    lsDomains = self.domains
    lsVars = self.variables
    dctAssignments = self.assignments
    dctAssignments[1].append('Brazil')
    dctAssignments[1].append('Mexico')
    if len(dctAssignments) == len(self.variables):
      return dctAssignments

    currentCountry = self.GetVar()
    for value in lsDomains[currentCountry]:
      if 0 == self.CheckConstraints(currentCountry, value, dctAssignments):
        print("Allowed in group: %d " % value)

  def MakeAssign(self):
    pass

  def GetVar(self):
    for country in self.variables:
      if country not in self.assignments:
        return country

  def Assign(self):
    pass

  def CheckConstraints(self, currentCountry, value, dctAssignments):
    #print("%s info: %s , %s " % (currentCountry, self.potNeighbors[currentCountry], self.confNeighbors[currentCountry]))
    constraints = 0
    if value in dctAssignments:
      for country in dctAssignments[value]:
        #print("%s info: %s , %s " % (country, self.potNeighbors[country], self.confNeighbors[country]))
        if self.potNeighbors[country] == self.potNeighbors[currentCountry] or \
          self.confNeighbors[country] == self.confNeighbors[currentCountry]:
          constraints = constraints + 1

        elif self.potNeighbors[country] != self.potNeighbors[currentCountry] and \
          self.confNeighbors[country] != self.confNeighbors[currentCountry]:
          return 0

    return constraints


