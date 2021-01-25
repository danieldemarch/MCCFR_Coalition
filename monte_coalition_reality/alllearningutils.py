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


def handle_conglomeration_boogaloo(poser_pies, poser_pols, posers, thepower):
    
    final_pies = poser_pies.copy()
    final_pols = poser_pols.copy()
    
    poser_dupe = posers.copy()
    
    pie_bools = np.zeros((len(posers), len(posers)))
    
    ticker = 0
    for i in range(len(posers)):
        if(posers[i] == 1):
            pie_bools[i] = (poser_pies[ticker] > 0)
            ticker+=1
            
    #okay so we're going to fucking fix this.
    #putin_votes gets made at the beginning. roll everything from there.
    
    putin_votes = np.zeros((len(posers)))
    ticker=0
    for i in range(len(posers)):
        if(posers[i] == 0):
            putin_votes[i] = -1
        else:
            putin_votes[i] = ticker
            ticker+=1
            
    unique_pies = np.unique(pie_bools, axis=0)
    
    unique_pies = unique_pies[~np.all(unique_pies == 0, axis=1)]
    conglom_pies = []    
    
    for i in range(len(unique_pies)):
        nopose_cond = (poser_dupe==0)
        poser_cond = (pie_bools == unique_pies[i]).all(axis=1)
        the_mask = np.logical_or(nopose_cond, poser_cond)
        not_it = (unique_pies[i] == 0)
        
        better_together = np.logical_or(the_mask, not_it)
        
        boolval = np.count_nonzero((unique_pies[i].astype(bool)[posers.astype(bool)]))
        
        if((better_together == True).all() and boolval>1):
            conglom_pies.append(unique_pies[i])
            
    conglom_pies = np.array(conglom_pies)
    conglom_firstindex = np.zeros((len(conglom_pies))).astype(int)
    
    for i in range(len(conglom_pies)):
        ticker = 0
        for j in range(len(poser_pies)):
            if(np.array_equal(conglom_pies[i], (poser_pies[j] > 0))):
                conglom_firstindex[i] = j
                break
    
    for i in range(len(conglom_pies)):
        conglomlist = []
        pollist = []
        for j in range(len(poser_pies)):
            if(np.array_equal((poser_pies[j] > 0).astype(int), conglom_pies[i])):
               conglomlist.append(poser_pies[j])
               pollist.append(poser_pols[j])
               
        conglomlist = np.array(conglomlist)
        
        finalpie = np.zeros((len(posers)))
        finalpol = np.zeros((len(poser_pols[0])))
        powsum = np.sum(thepower[(conglom_pies[i]>0)])
        
        poser_powers = thepower[np.logical_and((conglomlist[0] > 0), (posers > 0))]
        
        for j in range(len(conglomlist)):
            finalpie = conglomlist[j]*poser_powers[j]
            
        finalpie = finalpie/np.sum(finalpie)
    
        for j in range(len(pollist)):
            finalpol+=pollist[j]*thepower[j]
            
        finalpol = np.rint(finalpol/powsum)
        
        final_pies[conglom_firstindex[i]] = finalpie
        final_pols[conglom_firstindex[i]] = finalpol
    
    for i in range(len(conglom_firstindex)):
        for j in range(len(final_pies)):
            if(np.array_equal(conglom_pies[i], (final_pies[j] > 0)) and j > conglom_firstindex[i]):
                final_pies[j] = np.full((len(final_pies[j])), -100)
                putin_votes[(putin_votes == j)] = conglom_firstindex[i]
                

    return final_pies, final_pols, putin_votes.astype(int)

def handle_voting(putin_votes, poser_pies, poser_pols, thereversion, thepolicy, thesalience, thepower):
    
    votes = np.zeros((len(poser_pies)+1))
                
    for i in range(len(putin_votes)):
        
        if(putin_votes[i] == -1):
            rewardvec = np.full((len(votes)), thereversion, dtype=float)
                        
            for j in range(len(poser_pies)):
                rewardvec[j] += calculatereward(thepolicy[i], thesalience[i], poser_pols[j], poser_pies[j][i])
            
            votes[np.argmax(rewardvec)]+=thepower[i]
        #     if(np.argmax(rewardvec) < len(poser_pies)):
        #         print(i, rewardvec, thepolicy[i], thesalience[i], poser_pols[np.argmax(rewardvec)], poser_pies[np.argmax(rewardvec)])
        #     else:
        #         print(i, rewardvec)
        else:
            votes[putin_votes[i]]+=thepower[i]
        
    return votes



















