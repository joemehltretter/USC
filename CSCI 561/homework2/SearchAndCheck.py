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

    #strCurrentCountry = self.GetVarMRV(lsVariables, dctAssignments)
    lsVariables = self.GetVarMRV(lsVariables, dctAssignments)
    print("About to go through variables, size: %d " % len(lsVariables))
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
          removed = self.MakeInferenceFromRemoval(strCurrentCountry, value)
          self.removed = removed
          queueAc3 = [(strCurrentCountry, neighbor) for neighbor in self.csp.neighboringCountries[strCurrentCountry]]
          arcConsistent = self.ArcConsistency3(queueAc3)
          if arcConsistent:
            solution = self.BacktrackSearch(dctAssignments)
            if solution != None:
              print("Solution is not none")
              return solution
          print("\nIs not arc consistent: %s " % arcConsistent)
          self.csp.Undo(removed)

    dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
    #dctAssignments = self.csp.RemoveAssignment(strCurrentCountry, dctAssignments)
    return None


  def ArcConsistency3(self, queueToCheck=None):
    #Check is toCheck queue is empty
    if not queueToCheck:
      print("In not queue check #######################")
      for getCountry in self.csp.variables:
        for neighbor in self.csp.neighboringCountries[getCountry]:
          queueToCheck.append([getCountry, neighbor])
    print("\nCurrent queue: %s " % queueToCheck)
    self.PruneDomainValues()
    while queueToCheck:
      (country, neighbor) = queueToCheck.pop()
      if not self.csp.notConstrainedDomains[country]:
        print("%s : %s " % (country, self.csp.notConstrainedDomains[country]))
        return False
      print("\tPerforming AC3 for %s on neighbor %s " % (country, neighbor))
      pruneDone = self.CheckForPrunes(country, neighbor)
      print("\tPrune done value is: %s " % pruneDone)
      if pruneDone:
        #if not self.csp.notConstrainedDomains[neighbor]:
          #print("%s : %s " % (neighbor, self.csp.notConstrainedDomains[neighbor]))
          #return False
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
    for domainValue in self.csp.notConstrainedDomains[neighbor]:
      if all(not self.csp.CheckDirectConstraint(neighbor, domainValue, currentCountry, value) for value in self.csp.notConstrainedDomains[currentCountry]):
        self.MakePrune(neighbor, domainValue)
        prunesAvailable = True

    return prunesAvailable

  def MakePrune(self, country, value):
    print("\t \tBefore prune %s: %s " % (country, self.csp.notConstrainedDomains[country]))
    self.csp.notConstrainedDomains[country].remove(value)
    print("\t \tAfter prune %s: %s " % (country, self.csp.notConstrainedDomains[country]))
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