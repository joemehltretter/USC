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
    self.notConstrainedDomains = collections.defaultdict(list)
    self.constraintCount = 0
    self.potNeighbors = potNeighbors
    self.confNeighbors = confNeighbors
    self.constraints = constraints
    self.assignCount = 0
    self.assignments = collections.defaultdict(list)
    self.consCheck = collections.defaultdict(list)

  def Solve(self, dctAssignments):
    lsVariables = self.variables
    if len(dctAssignments) == len(self.valInfo):
      for key in dctAssignments.keys():
        print("%s : % s" % (key, dctAssignments[key]))
      return dctAssignments

    strCurrentCountry = self.GetVarMRV(lsVariables, dctAssignments)
    if self.notConstrainedDomains[strCurrentCountry]:
      lsReorderedVals = self.notConstrainedDomains[strCurrentCountry]
    else:
      lsReorderedVals = self.domains[strCurrentCountry]

    for value in lsReorderedVals:
      if 0 == self.CheckConstraints(strCurrentCountry, value):
        dctAssignments = self.MakeAssign(strCurrentCountry, value, dctAssignments)
        solution = self.Solve(dctAssignments)
        if strCurrentCountry in lsVariables:
          lsVariables.remove(strCurrentCountry)
        if solution is not None:
          return solution

    self.RemoveAssginment(strCurrentCountry, dctAssignments)
    return None

  def RemoveAssginment(self, country, assignments):
    if country in assignments:
      del assignments[country]
    return assignments

  def MakeAssign(self, country, group, assignments):
    assignments[country].append(group)
    self.consCheck[group].append(country)
    return assignments

  def GetVarMRV(self, variables, assignments):
    dctCount = collections.defaultdict(list)
    for country in variables:
      if country not in assignments:
        if self.notConstrainedDomains[country]:
          dctCount[country] = len(self.notConstrainedDomains[country])
        else:
          dctCount[country] = len(self.domains)
    mrv = min(dctCount, key=dctCount.get)
    return mrv


  def CheckConstraints(self, currentCountry, value):
    constraints = 0
    if value in self.consCheck:
      for country in self.consCheck[value]:
        #print("\n%s info: %s , %s " % (currentCountry, self.potNeighbors[currentCountry], self.confNeighbors[currentCountry]))
        #print("%s info: %s , %s " % (country, self.potNeighbors[country], self.confNeighbors[country]))
        if self.potNeighbors[country] == self.potNeighbors[currentCountry]:
          constraints = constraints + 1

        elif self.confNeighbors[country] == self.confNeighbors[currentCountry]:
          constraints = constraints + 1

    return constraints


