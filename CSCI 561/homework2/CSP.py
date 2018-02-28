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
    print("\tCountry assigned before this one was: %s " % self.assignOrder[-1])
    country = self.assignOrder[-1]
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

  def CheckDirectConstraint(self, c1, c1Val, c2, c2Val):
    if((c1Val == c2Val) and ('UEFA' in self.valInfo[c1]) and ('UEFA' in self.valInfo[c2])):
      return False
    if((c1Val == c2Val) and (('UEFA' in self.valInfo[c1]) or ('UEFA' in self.valInfo[c2]))):
      #print("\t \tEither %s or %s are in UEFA so checking additional constraint." % (c1, c2))
      count = 0
      for country in self.assignments.keys():
        if "UEFA" in self.valInfo[country] and self.assignments[country] == c1Val:
          count = count + 1
      if count < 2:
        #print("\t%d country(ies) in pot %s" % (count, c2Val))
        return True
      else:
        #print("\t%d country(ies) in pot %s" % (count, c2Val))
        return False
    elif c1Val == c2Val:
      return False
    return True

  def CheckConstraints(self, currentCountry, value, assignments):
    constraints = 0
    uefaCount = 0
    for country, checkValue in assignments.iteritems():
      if value == checkValue:
        if 'UEFA' in self.valInfo[country] and 'UEFA' in self.valInfo[currentCountry]:
          print("Both UEFA")
          uefaCount = uefaCount + 1
          if uefaCount >= 2:
            return 2
        elif country in self.neighboringCountries[currentCountry]:
          constraints = 1
    return constraints


