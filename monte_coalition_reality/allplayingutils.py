#player tree generation file
import numpy
import random
import math
import itertools
from numba import jit

#generates all combinations of powers

def makepowercombinations(powervec):
    powertest = []
    for i in range(len(powervec)):
      powertest.append(powervec[i]+i/100)
    result = [seq for i in range(len(powertest), 0, -1) for seq in itertools.combinations(powertest, i)]
    return result, powertest

def makepossibleplayercoalitions(powercombinations, powertest):
    possiblecoalitions = []
    for i in range(len(powercombinations)):
      dumbcoalition = powercombinations[i]
      coalition = []
      for j in range(len(dumbcoalition)):
        coalition.append(powertest.index(dumbcoalition[j]))
      coalition = numpy.array(coalition)
      if(numpy.any(coalition == 0)):
          possiblecoalitions.append(coalition)
    return possiblecoalitions


def makeallpossiblecoalitions(powercombinations, powertest):
    possiblecoalitions = []
    for i in range(len(powercombinations)):
      dumbcoalition = powercombinations[i]
      coalition = []
      for j in range(len(dumbcoalition)):
        coalition.append(powertest.index(dumbcoalition[j]))
      coalition = numpy.array(coalition)
      possiblecoalitions.append(coalition)
    return possiblecoalitions

def partitions(n, b):
    masks = numpy.identity(b, dtype=int)
    for c in itertools.combinations_with_replacement(masks, n): 
        yield sum(c)

def makepossiblepieslices(actors, numdivisions):
    boxes = actors
    balls = numdivisions
        
    iterset = numpy.array(list(partitions(balls, boxes)))
        
    finallist = []
    for j in range(len(iterset)):
        arr = numpy.array(iterset[j])
        arr = arr/(balls)
        finallist.append((numpy.array(iterset[j]))/numdivisions)
            
    finallist = numpy.array(finallist)
        
    return finallist

def makeplayerpies(pielist, numactors):
    allplayerpies = []
    for i in range(numactors):
        playerpies = []
        for j in range(len(pielist)):
            if(pielist[j][i] > 0):
                playerpies.append(pielist[j])
        allplayerpies.append(playerpies)
            
    return allplayerpies
    
def makesinglepolicy(arr, n):  
    dummy = numpy.zeros((len(arr)))
    for i in range(0, n):  
        dummy[i] = arr[i]
      
    return dummy

def generateallpolicystrings(n, arr, i, policylist):  
    if i == n: 
        policy = makesinglepolicy(arr, n)  
        policylist.append(policy)
        return
    
    arr[i] = 0
    generateallpolicystrings(n, arr, i + 1, policylist)  
    arr[i] = 1
    generateallpolicystrings(n, arr, i + 1, policylist) 

def returnallpolicystrings(numpolicies):
    arr = [None] * numpolicies
    policylist = []
    generateallpolicystrings(numpolicies, arr, 0, policylist)
    return numpy.array(policylist)


        
    








