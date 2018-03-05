import collections
import copy
import random

class SearchAndCheck(object):
  def __init__(self, cspObject):
    self.csp = cspObject
    self.removed = []

  #Hill climbing's randomization will be useful in large problems as backtracking seems to loop causing time issues.
  def HillClimbing(self, steps, dctAssignments):
    lsVariables = self.csp.variables
    toChange = []

    for country in lsVariables:
      if self.csp.notConstrainedDomains:
        lsReorderedVals = self.OrderValues(self.csp.notConstrainedDomains[country], dctAssignments)
      else:
        lsReorderedVals = self.OrderValues(self.csp.domains[country], dctAssignments)
      if len(lsReorderedVals):
        dctAssignments[country] = lsReorderedVals.pop(0)

    #Once all variables have been assigned go through and find conflicts and change assignments
    for step in range(steps):
      conflict = False
      random.shuffle(lsVariables)
      for randomToChangeCountry in lsVariables:
        if self.csp.CountryConstraints(randomToChangeCountry, dctAssignments) == 0:
          continue
        minConstraintCount = self.csp.CountryConstraints(randomToChangeCountry, dctAssignments)
        minConstrainedGroups = []
        for group in self.csp.domains[randomToChangeCountry]:
          dctAssignments[randomToChangeCountry] = group
          constraintCount = self.csp.CountryConstraints(randomToChangeCountry, dctAssignments)
          if constraintCount == minConstraintCount:
            minConstrainedGroups.append(group)
          elif constraintCount < minConstraintCount:
            minConstraintCount = constraintCount
            del minConstrainedGroups[:]
            minConstrainedGroups.append(group)
        groupToChange = random.choice(minConstrainedGroups)
        dctAssignments[randomToChangeCountry] = groupToChange
        conflict = True
      if not conflict:
        return dctAssignments
    #If problem gets to this point no solution so return None
    return None

  #Fast for smaller problems so use for those.
  def BacktrackSearch(self, dctAssignments, consistencyCheck):
    lsVariables = self.csp.variables
    if len(dctAssignments) == len(self.csp.valInfo):
      return dctAssignments
    if len(dctAssignments) == 0:
      length = 0
      for country, neighbors in self.csp.neighboringCountries.iteritems():
        if len(neighbors) > length:
          length = len(neighbors)
          strCurrentCountry = country

    else:
      strCurrentCountry = self.GetVarMRV(lsVariables, dctAssignments)

    if len(dctAssignments) == 0:
      lsReorderedVals = self.csp.domains[strCurrentCountry]
    else:
      if self.csp.notConstrainedDomains:
        lsReorderedVals = self.OrderValues(self.csp.notConstrainedDomains[strCurrentCountry], dctAssignments)
      else:
        lsReorderedVals = self.OrderValues(self.csp.domains[strCurrentCountry], dctAssignments)

    for value in lsReorderedVals:
      if 0 == self.csp.CheckConstraints(strCurrentCountry, value, dctAssignments):
        dctAssignments = self.csp.MakeAssignment(strCurrentCountry, value, dctAssignments)
        # Begin Inference
        removed = self.MakeInferenceFromRemoval(strCurrentCountry, value)
        self.removed = removed
        consistent = self.consistent(strCurrentCountry, value, dctAssignments)
        if consistent:
          solution = self.BacktrackSearch(dctAssignments, consistencyCheck)
          if solution != None:
            return solution
        self.csp.Undo(removed)

    self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
    return None

  def CheckForPrunes(self, neighbor, currentCountry):
    prunesAvailable = False
    for domainValue in self.csp.notConstrainedDomains[currentCountry]:
      if all(not self.csp.IsConstrained(currentCountry, domainValue, neighbor, value) for value in self.csp.notConstrainedDomains[neighbor]):
        self.MakePrune(neighbor, value)
        prunesAvailable = True
    return prunesAvailable

  def consistent(self, country, value, assignments):
    for neighbor in self.csp.neighboringCountries[country]:
      if neighbor not in assignments:
        for possibleValue in self.csp.notConstrainedDomains[neighbor]:
          constrained = self.csp.IsConstrained(country, value, neighbor, possibleValue)
          if constrained:
            self.MakePrune(neighbor, possibleValue)
        if neighbor in self.csp.notConstrainedDomains:
          if not self.csp.notConstrainedDomains[neighbor]:
            return False
    return True

  def MakeInferenceFromRemoval(self, country, valueAssigned):
    self.PruneSetup()
    removed = [(country, value) for value in self.csp.notConstrainedDomains[country] if value != valueAssigned]
    self.csp.notConstrainedDomains[country] = [valueAssigned]
    return removed

  def MakePrune(self, country, value):
    self.csp.notConstrainedDomains[country].remove(value)
    if self.removed is not None:
      self.removed.append((country, value))

  def PruneSetup(self):
    if not self.csp.notConstrainedDomains:
      self.csp.notConstrainedDomains = {variable: list(self.csp.domains[variable]) for variable in self.csp.variables}

  def OrderValues(self, domainInfo, dctAssignments):
    if len(domainInfo) == 1:
      return domainInfo
    dctValInfo = collections.defaultdict(list)
    lsOrderedValues = []
    for country, value in dctAssignments.iteritems():
      if value in domainInfo:
        dctValInfo[value].append(1)
    for value in sorted(dctValInfo, key=lambda value: len(dctValInfo[value]), reverse=True):
      lsOrderedValues.append(value)
    if len(lsOrderedValues) == 0 and len(domainInfo) != 0:
      lsOrderedValues = domainInfo
    return lsOrderedValues

  def GetVarMRV(self, variables, dctAssignments):
    dctCount = []
    for var in variables:
      if var not in dctAssignments:
        variable = var
        break

    mrv = variable
    dctConstraintCount = self.csp.GetConstraintCount(variables, dctAssignments)
    dctCount.append(variable)
    for country, count in dctConstraintCount.iteritems():
      if country != variable:
        if dctConstraintCount[country] > dctConstraintCount[variable]:
          variable = country
          dctCount.pop(0)
          dctCount.append(country)
        elif dctConstraintCount[country] == dctConstraintCount[variable]:
          dctCount.append(country)
    if len(dctCount) == 1:
      mrv = dctCount[0]
    elif len(dctCount) > 1:
      mrv = dctCount.pop(0)
      if mrv in self.csp.notConstrainedDomains:
        mrvCount = len(self.csp.notConstrainedDomains[mrv])
      else:
        mrvCount = len(self.csp.domains[mrv])
      for checkCountry in dctCount:
        if checkCountry in self.csp.notConstrainedDomains:
          cCount = len(self.csp.notConstrainedDomains[checkCountry])
        else:
          cCount = len(self.csp.domains[checkCountry])
        if cCount <= mrvCount:
          mrvCount = cCount
          mrv = checkCountry
    return mrv
