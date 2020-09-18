#player tree generation file
import numpy as np
import random
from numba import jit
from calculationutils import *

@jit(nopython=True, fastmath=True)
def handleblackboxvoting(thepower, thepolicy, thesalience, policies, pies, thereversion):
    votes = np.zeros((len(pies)))
        
    for j in range(1, len(thepower)):
                
                #casts ai player votes by filling in rewards, casting vote for highest one
                rewardvec= np.full((len(votes)), thereversion)
                
                for i in range(len(policies)):
                    rewardvec[i] = calculatereward(thepolicy[j], thesalience[j], policies[i], 0)
                
                for i in range(len(pies)):
                    for k in range(len(pies[i])):
                        if(k==j):
                            rewardvec[i]+=(pies[i, k])/2
                            break

                votes[np.argmax(rewardvec)]+=thepower[j]
            
    return votes

def creationofcoalitions(playerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience):    
    
    piebucket = checkbucket_pie(playerpieprobs)
    playerpie = playerpies[piebucket]
    #finally decide policys
    correspondingpolicyprob = playerpolicyprobs[piebucket]
    
    policybucket = checkbucket_policy(correspondingpolicyprob)
    playerpolicy = thepossiblepolicies[policybucket]
    
    #calculate your potential reward from this action
    possiblereward = calculatereward(thepolicy[0], thesalience[0], playerpolicy, playerpie[0])
    
    #return proposed coalition, policy, pie, reward, coalbucket, coalsize
    
    return playerpie, playerpolicy, possiblereward, piebucket, policybucket


#@jit(nopython=True, fastmath=True)
#@jit()
def playercreatespath(coalresults, pieresults, polresults, playerreward, aipies, aipolicies, playerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience, thepower):
    playerpie, playerpolicy, possiblereward, piebucket, policybucket = creationofcoalitions(playerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience)
    
    fullpies = np.zeros(((len(aipies)+1), len(aipies[0])))
    fullpolicies = np.zeros(((len(aipolicies)+1), len(aipolicies[0])))
                
    fullpies[0:len(aipies)] = aipies
    fullpolicies[0:len(aipolicies)] = aipolicies
    
    fullpies[len(fullpies)-1] = playerpie
    fullpolicies[len(fullpolicies)-1] = playerpolicy
    
    votes = handleblackboxvoting(thepower, thepolicy, thesalience, fullpolicies, fullpies, thereversion)
                    
    #player auto-votes for their own        
    votes[len(votes)-1]+=thepower[0]
        
    #calcs power to beat and checks if any votes exceed this value
    powtobeat = (np.sum(thepower))/2
        
    awin = 0
    windex = -1
        
    for j in range(len(votes)):
        if(votes[j] > powtobeat):
            awin = 1
            windex = j
            break
                
    if(awin==0):
        playerreward = thereversion
    else:
        pieval = fullpies[windex, 0]
        playerreward = calculatereward(thepolicy[0], thesalience[0], fullpolicies[windex], pieval)
        
    return piebucket, policybucket, playerreward









