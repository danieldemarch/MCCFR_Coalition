from calculationutils import *
from allplayingutils import *
import numpy as np

def find_posers(playerproposeprobs):
    posers = np.zeros((len(playerproposeprobs)))
    for i in range(len(posers)):
        poser = checkbucket_proposal(playerproposeprobs[i])
        
        posers[i] = poser
    
    return posers

def creationofcoalitions(playerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience):    
    
    piebucket = checkbucket_pie(playerpieprobs)
    playerpie = playerpies[piebucket]
    
    #finally decide policys
    correspondingpolicyprob = playerpolicyprobs[piebucket]
    
    policybucket = checkbucket_policy(correspondingpolicyprob)
    playerpolicy = thepossiblepolicies[policybucket]
                
    return playerpie, playerpolicy, piebucket, policybucket

def get_poser_coalitions(posers, pies, pieprobs, thepossiblepolicies, policyprobs, thereversion, thepolicy, thesalience):
    
    poserlist = np.where(posers==1)[0]
    
    poser_pies = np.zeros((len(poserlist), len(pies[0][0])))
    poser_pols = np.zeros((len(poserlist), len(thepolicy[0])))
    poser_piebuckets = np.zeros((len(poserlist)))
    poser_policybuckets = np.zeros((len(poserlist)))
    
    for i in range(len(poserlist)):
        
        index = poserlist[i]
        playerpie, playerpolicy, piebucket, policybucket = creationofcoalitions(pies[index], pieprobs[index], thepossiblepolicies, policyprobs[index], thereversion, thepolicy, thesalience)
        poser_pies[i] = playerpie
        poser_pols[i] = playerpolicy
        poser_piebuckets[i] = piebucket
        poser_policybuckets[i] = policybucket
        
    return poser_pies, poser_pols, poser_piebuckets, poser_policybuckets

def handle_voting(posers, poser_pies, poser_pols, thereversion, thepolicy, thesalience, thepower):
    poserlist = np.where(posers==1)[0]
    mainstreamlist = np.where(posers==0)[0]
    
    if(len(poserlist) == 0):
        return np.full((len(posers)), thereversion)
        
    votes = np.zeros((len(poser_pies)))
    
    for i in range(len(poserlist)):
        votes[i]+=thepower[poserlist[i]]
                
    for i in range(len(mainstreamlist)):
        rewardvec = np.zeros((len(poserlist)))
        
        person = mainstreamlist[i]
        
        for j in range(len(rewardvec)):
            rewardvec[j] = calculatereward(thepolicy[person], thesalience[person], poser_pols[j], poser_pies[j][mainstreamlist[i]])
        votes[np.argmax(rewardvec)]+=thepower[mainstreamlist[i]]
        
    return votes



















