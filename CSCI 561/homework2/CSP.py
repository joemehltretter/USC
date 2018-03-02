#####################################################################
#                                                                   #
# CSP.py will be the file that does all the CSP work to solve the   #
# problem.                                                          #
#                                                                   #
#####################################################################
import collections
import SearchAndCheck
import copy

class CSP(object):
  def __init__(self, variables, variableInfo, domains, neighbors, constraints):
    self.variables = variables
    self.valInfo = variableInfo
    self.domains = domains
    self.notConstrainedDomains = None
    self.constraintCount = 0
    self.neighboringCountries = neighbors
    self.constraints = constraints
    self.assignOrder = []
    self.assignments = {}
    self.consCheck = collections.defaultdict(list)

  def RemoveAssignment(self, country, assignments):
    if country in assignments:
      del self.assignments[country]
    return self.assignments

  def MakeAssignment(self, country, group, assignments):
    self.assignments[country] = group
    #assignments[country] = group
    self.assignOrder.append(country)
    return self.assignments

  def Undo(self, lsRemoved):
    for removedCountry, removedValue in lsRemoved:
      self.notConstrainedDomains[removedCountry].append(removedValue)

  def IsConstrained(self, country, cValue, neighbor, nValue):
    if ((cValue == nValue) and (self.valInfo[country][0] == self.valInfo[neighbor][0])):
      return True
    elif ((cValue == nValue) and ('UEFA' in self.valInfo[neighbor])):
      uefaCount = 0
      for country, value in self.assignments.iteritems():
        if ((value == cValue) and ('UEFA' in self.valInfo[country])):
          uefaCount = uefaCount + 1
      if uefaCount < 2:
        return False
      else:
        return True
    elif cValue == nValue:
      return True

    return False

  def GetConstraintCount(self, variables, assignments):
    valInfo = copy.deepcopy(self.valInfo)
    dctConstraints = {}
    for country in variables:
      constraints = 0
      possVals = self.domains[country]
      if country not in assignments:
        for value in possVals:
          uefaCount = 0
          uefaFlip = False
          for checkCountry, checkValue in assignments.iteritems():
            if value == checkValue and valInfo[country][0] == valInfo[checkCountry][0]:
              constraints = constraints + 1
            if value == checkValue and valInfo[country][1] == valInfo[checkCountry][1]:
              if 'UEFA' in valInfo[checkCountry][1]:
                uefaCount = uefaCount + 1
              elif ('UEFA' not in valInfo[checkCountry][1]):
                constraints = constraints + 1
            if ((uefaCount == 2) and ('UEFA' in valInfo[country][1])):
              if uefaFlip == False:
                constraints = constraints + 1
                uefaFlip = True
        dctConstraints[country] = constraints

    return dctConstraints

  def CheckConstraints(self, currentCountry, value, assignments):
    constraints = 0
    uefaCount = 0
    for country, checkValue in assignments.iteritems():
      if value == checkValue:
        if self.valInfo[country][0] == self.valInfo[currentCountry][0]:
          return 1
        elif ((self.valInfo[country][1] == self.valInfo[currentCountry][1]) and ('UEFA' not in self.valInfo[country][1])):
          return 1
        elif ((self.valInfo[country][1] == self.valInfo[currentCountry][1]) and ('UEFA' in self.valInfo[country][1])):
          uefaCount = uefaCount + 1
        if uefaCount >= 2:
          return 1
    return constraints



