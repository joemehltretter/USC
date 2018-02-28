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
    self.assignCount = 0
    self.assignments = {}
    self.consCheck = collections.defaultdict(list)

  def RemoveAssignment(self, country, assignments):
    print("Before removal assignments are: %s " % assignments)
    if country in assignments:
      print("\nConstraint issue so removing %s assignment of %s " % (country, assignments[country]))
      del self.assignments[country]
      del assignments[country]
    print("Therefore, current assignments are: %s " % assignments)

  def MakeAssignment(self, country, group, assignments):
    #print("\nAssigning %s to %s. " % (group, country))
    self.assignments[country] = group
    assignments[country] = group
    self.consCheck[group].append(country)
    #print("Making current assignments: %s " % assignments)
    return assignments

  def Undo(self, lsRemoved):
    print("\n Constraint issue so resetting removed queue from: %s " % self.notConstrainedDomains)
    for country, value in lsRemoved:
      if value not in self.notConstrainedDomains[country]:
        self.notConstrainedDomains[country].append(value)
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

  def CheckConstraints(self, currentCountry, value):
    constraints = 0
    assignments = self.assignments

    for neighbor in self.neighboringCountries[currentCountry]:
      if neighbor in assignments.keys():
        if assignments[neighbor] == value:
          return 1
      if neighbor not in assignments.keys():
        continue
    return constraints


