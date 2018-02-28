import collections

class SearchAndCheck(object):
  def __init__(self, cspObject):
    self.csp = cspObject
    self.removed = []

  def BacktrackSearch(self, dctAssignments):
    lsVariables = self.csp.variables
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(len(dctAssignments), len(self.csp.valInfo))
    if len(dctAssignments) == len(self.csp.valInfo):
      return dctAssignments

    strCurrentCountry = self.GetVarMRV(lsVariables, dctAssignments)
    print("About to go through variables, size: %d " % len(lsVariables))
    print("******** Current Country: %s*******************\n" % strCurrentCountry)
    if self.csp.notConstrainedDomains:
      lsReorderedVals = self.csp.notConstrainedDomains[strCurrentCountry]
    else:
      lsReorderedVals = self.csp.domains[strCurrentCountry]

    for value in lsReorderedVals:
      if 0 == self.csp.CheckConstraints(strCurrentCountry, value, dctAssignments):
        dctAssignments = self.csp.MakeAssignment(strCurrentCountry, value, dctAssignments)
        # Begin Inference
        removed = self.MakeInferenceFromRemoval(strCurrentCountry, value)
        self.removed = removed
        #queueAc3 = [(strCurrentCountry, neighbor) for neighbor in self.csp.neighboringCountries[strCurrentCountry]]
        #consistent = self.ArcConsistency3([])
        consistent = self.consistent(strCurrentCountry, value, dctAssignments)
        #print("\t Is value consistent? %s " % consistent)
        if consistent:
          solution = self.BacktrackSearch(dctAssignments)
          if solution != None:
            return solution
        self.csp.Undo(removed)

    dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
    #dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
    return None

  def consistent(self, country, value, assignments):
    print("Checking consistency of value %s for country %s with neighbors %s " % (value, country, self.csp.neighboringCountries[country]))
    for neighbor in self.csp.neighboringCountries[country]:
      if neighbor not in assignments:
        for possibleValue in self.csp.notConstrainedDomains[neighbor]:
          print("\t Checking consistency of neighbor %s with value %s " % (neighbor, possibleValue))
          #constrained = self.csp.CheckDirectConstraint(country, value, neighbor, possibleValue)
          constrained = self.csp.IsConstrained(country, value, neighbor, possibleValue)
          if constrained:
            self.MakePrune(neighbor, possibleValue)
        if neighbor not in self.csp.notConstrainedDomains:
          return False
    return True

  def ArcConsistency3(self, queueToCheck=None):
    #Check is toCheck queue is empty
    if queueToCheck is None:
      for getCountry in self.csp.variables:
        for neighbor in self.csp.neighboringCountries[getCountry]:
          queueToCheck.append([getCountry, neighbor])
    self.PruneDomainValues()
    while queueToCheck:
      (country, neighbor) = queueToCheck.pop()
      if not self.csp.notConstrainedDomains[country]:
        print("%s : %s " % (country, self.csp.notConstrainedDomains[country]))
        return False
      pruneDone = self.CheckForPrunes(country, neighbor)
      if pruneDone:
        if not self.csp.notConstrainedDomains[neighbor]:
          print("%s : %s " % (neighbor, self.csp.notConstrainedDomains[neighbor]))
          return False
        for newNeighbor in self.csp.neighboringCountries[neighbor]:
          if neighbor != newNeighbor:
            queueToCheck.append((neighbor, newNeighbor))
    return True

  def MakeInferenceFromRemoval(self, country, valueAssigned):
    self.PruneDomainValues()
    removed = [(country, value) for value in self.csp.notConstrainedDomains[country] if value != valueAssigned]
    self.csp.notConstrainedDomains[country] = [valueAssigned]
    return removed

  def CheckForPrunes(self, currentCountry, neighbor):
    prunesAvailable = False
    for domainValue in self.csp.notConstrainedDomains[currentCountry]:
      if all(not self.csp.IsConstrained(currentCountry, domainValue, neighbor, value) for value in self.csp.notConstrainedDomains[neighbor]):
        self.MakePrune(currentCountry, domainValue)
        prunesAvailable = True

    return prunesAvailable

  def MakePrune(self, country, value):
    self.csp.notConstrainedDomains[country].remove(value)
    if self.removed is not None:
      self.removed.append((country, value))

  def PruneDomainValues(self):
    if not self.csp.notConstrainedDomains:
      self.csp.notConstrainedDomains = {variable: list(self.csp.domains[variable]) for variable in self.csp.variables}

  def GetVarMRV(self, variables, dctAssignments):
    dctCount = collections.defaultdict(list)
    for country in variables:
      if country not in dctAssignments:
        if self.csp.notConstrainedDomains:
          dctCount[country] = len(self.csp.notConstrainedDomains[country])
        else:
          dctCount[country] = len(self.csp.domains[country])
    vars = []
    for country, value in sorted(dctCount.iteritems(), key=lambda (key, value): (value, key)):
      vars.append(country)
    mrv = min(dctCount, key=dctCount.get)
    return mrv