import collections

class SearchAndCheck(object):
  def __init__(self, cspObject):
    self.csp = cspObject
    self.removed = []

  def BacktrackSearch(self, dctAssignments):
    lsVariables = self.csp.variables
    if len(dctAssignments) == len(self.csp.valInfo):
      return dctAssignments

    #strCurrentCountry = self.GetVarMRV(lsVariables, dctAssignments)
    lsVariables = self.GetVarMRV(lsVariables, dctAssignments)
    for strCurrentCountry in lsVariables:
      print("******** Current Country: %s*******************\n" % strCurrentCountry)
      if self.csp.notConstrainedDomains:
        lsReorderedVals = self.csp.notConstrainedDomains[strCurrentCountry]
      else:
        lsReorderedVals = self.csp.domains[strCurrentCountry]

      for value in lsReorderedVals:
        if 0 == self.csp.CheckConstraints(strCurrentCountry, value):
          dctAssignments = self.csp.MakeAssignment(strCurrentCountry, value, dctAssignments)
          # Begin Inference
          self.MakeInferenceFromRemoval(strCurrentCountry, value)
          queueAc3 = [(strCurrentCountry, neighbor) for neighbor in self.csp.neighboringCountries[strCurrentCountry]]
          if self.ArcConsistency3(queueAc3):
            solution = self.BacktrackSearch(dctAssignments)
            if solution is not None:
              return solution

          self.csp.Undo(self.removed)
      dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
      print("%s was unassignable %s " % (strCurrentCountry, dctAssignments))
      #dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
      return None


  def ArcConsistency3(self, queueToCheck=None):
    #Check is toCheck queue is empty
    if not queueToCheck:
      for getCountry in self.csp.variables:
        for neighbor in self.csp.neighboringCountries[getCountry]:
          queueToCheck.append([getCountry, neighbor])
    #print("Current queue: %s " % queueToCheck)
    self.PruneDomainValues()
    while queueToCheck:
      (country, neighbor) = queueToCheck.pop()
      #print("\tPerforming AC3 for %s on neighbor %s " % (country, neighbor))
      pruneDone = self.CheckForPrunes(country, neighbor)
      #print("Prune done value is: %s " % pruneDone)
      if pruneDone:
        if not self.csp.notConstrainedDomains[country]:
          return False
        for newNeighbor in self.csp.neighboringCountries[country]:
          if neighbor != newNeighbor:
            queueToCheck.append((country, newNeighbor))

    return True

  def MakeInferenceFromRemoval(self, country, valueAssigned):
    self.PruneDomainValues()
    self.removed = [(country, value) for value in self.csp.notConstrainedDomains[country] if value != valueAssigned]
    self.csp.notConstrainedDomains[country] = [valueAssigned]

  def CheckForPrunes(self, currentCountry, neighbor):
    prunesAvailable = False
    for domainValue in self.csp.notConstrainedDomains[neighbor]:
      if all(not self.csp.CheckDirectConstraint(neighbor, domainValue, currentCountry, value) for value in self.csp.notConstrainedDomains[currentCountry]):
        self.MakePrune(neighbor, domainValue)
        prunesAvailable = True

    return prunesAvailable

  def MakePrune(self, country, value):
    #print("\tBefore prune %s: %s " % (country, self.csp.notConstrainedDomains[country]))
    self.csp.notConstrainedDomains[country].remove(value)
    #print("\tAfter prune %s: %s " % (country, self.csp.notConstrainedDomains[country]))
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
    return vars