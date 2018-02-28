#####################################################################
#                                                                   #
# CSP.py will be the file that does all the CSP work to solve the   #
# problem.                                                          #
#                                                                   #
#####################################################################
import collections
import SearchAndCheck

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
    print("\nBefore removal assignments are: %s " % assignments)
    print("Length of assignments: %s " % len(self.assignOrder))
    if len(self.assignOrder) != 0:
      country = self.assignOrder[-1]
      self.assignOrder.remove(country)
    if country in assignments:
      print("\tConstraint issue so removing %s assignment of %s " % (country, assignments[country]))
      del self.assignments[country]
      del assignments[country]
    print("\tTherefore, current assignments are: %s " % assignments)
    return assignments

  def MakeAssignment(self, country, group, assignments):
    print("\nAssigning %s to %s. " % (group, country))
    self.assignments[country] = group
    assignments[country] = group
    self.assignOrder.append(country)
    self.consCheck[group].append(country)
    print("\tMaking current assignments: %s \n" % assignments)
    return assignments

  def Undo(self, lsRemoved):
    print("\n Completed assignments resetting constrained domains from: %s " % self.notConstrainedDomains)
    for removedCountry, removedValue in lsRemoved:
      print(removedCountry, removedValue)
      self.notConstrainedDomains[removedCountry].append(removedValue)
    print("To: %s " % self.notConstrainedDomains)

  def IsConstrained(self, country, cValue, neighbor, nValue):
    print("\n################# IS CONSTRAINED CHECK #########################")
    print("Check if %s value of %s is constrained by %s value of %s " % (country, cValue, neighbor, nValue))

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

#    for country, checkValue in assignments.iteritems():
#      if value == checkValue:
#        if 'UEFA' in self.valInfo[country] and 'UEFA' in self.valInfo[currentCountry]:
#          print("Both UEFA")
#          uefaCount = uefaCount + 1
#          if uefaCount >= 2:
#            return 2
#        elif country in self.neighboringCountries[currentCountry]:
#          constraints = 1
#    return constraints


