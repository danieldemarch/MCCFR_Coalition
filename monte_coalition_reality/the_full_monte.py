from calculationutils import *
from allplayingutils import *
from alllearningutils import *
import numpy as np
import random

megalist = []
megalist2 = []

numactors = 5
numpolicies = 5
thereversion = 0.1
nbiggest = 2
numdivisions = 10
learningrate = 0.01
numiter = 5
num_traversals = 100
 
thepower =  np.array([298,245,47,43,36])

thepolicy = np.array([[.4380483, .3296399, .5229917, .5635718, .3501385],
                      [.7052631, .7849944, .7110862, .3950393, .7170345],
                      [.527401, .0720222, .1152355, .2296651, .0880886],
                      [.9322509, .2258065, .8292273, .2588235, .3615561],
                      [.1046911, .2036613, .4282297, .6639676, .2182141]])

thepolicy = np.rint(thepolicy)

thesalience = np.array([[.2509293, .1869814, .2004321, .1555792, .2060781],
                        [.2348272, .2148662, .1795192, .1534228, .2173646],
                        [.1711163, .2235634, .2347826, .1482056, .222332],
                        [.2711053, .1905687, .1841413, .1754983, .1786864],
                        [.2797414, .1992622, .1674438, .1518179, .2017347]])
    
thepies = makepossiblepieslices(numactors, numdivisions)
    
allplayerpies = makeplayerpies(thepies, numactors)

for i in range(len(allplayerpies)):
    allplayerpies[i] = np.array(allplayerpies[i])
    np.random.shuffle(allplayerpies[i])
    
thepossiblepolicies = returnallpolicystrings(numpolicies)

thepossibleposers = returnallpolicystrings(numactors)
        
for z in range(numiter):
    
    playerproposeprobs = []
    playerpieprobs = []
    playerpolicyprobs = []
    playerchoiceprobs = []
    
    for i in range(numactors):
        #playerproposeprobs.append(np.array([1-(thepower[i]/np.sum(thepower)), (thepower[i]/np.sum(thepower))]))

        playerproposeprobs.append(returnflatprobability(np.zeros((2))))
        playerpieprobs.append(returnflatprobability(allplayerpies[i]))
        policyprobs = []
        for j in range(len(playerpieprobs[i])):
            
            policyprobs.append(returnflatprobability(thepossiblepolicies))
        playerpolicyprobs.append(policyprobs)
    
    ticker = 0
    
    choicetoconverge = np.full((numactors), -1)
    pcpieconverge = np.full((numactors), -1)
    pcpoliconverge = np.full((numactors), -1)
    
    i = 0
    
    while((np.any(choicetoconverge == -1) or np.any(pcpieconverge == -1) or np.any(pcpoliconverge == -1)) and i < 20000):
        
        if(i%100 == 0):
            print(i)
            for j in range(numactors):
                print(playerproposeprobs[j][1], np.max(playerpieprobs[j]), np.max(playerpolicyprobs[j]), allplayerpies[j][np.argmax(playerpieprobs[j])])
            
                
                # if(i>0):
                #     print(poser_pies)
                #     print(poser_pols)
                #     print(votes)
        
        i+=1
        
        
        for j in range(num_traversals):
            
            rewardvec = np.zeros((numactors))
            pieindexlist = np.zeros((numactors))
            policyindexlist = np.zeros((numactors))
            
            posers = find_posers(playerproposeprobs)
            
            while(np.count_nonzero(posers) < 1):
                posers = find_posers(playerproposeprobs)
            
            poser_pies, poser_pols, poser_piebuckets, poser_policybuckets = get_poser_coalitions(posers, allplayerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience)
            
            final_pies, final_pols, putin_votes = handle_conglomeration_boogaloo(poser_pies, poser_pols, posers, thepower)
            
            votes = handle_voting(putin_votes, final_pies, final_pols, thereversion, thepolicy, thesalience, thepower)
            
            windex = -1
            for k in range(len(votes)):
                
                if(votes[k] >= np.ceil(np.sum(thepower)/2)):
                    windex = k
                    break 
            
            if(windex == -1):
                
                for k in range(numactors):
                    rewardvec[k] = thereversion
                    
            elif(windex == len(poser_pies)):
                
                for k in range(numactors):
                    rewardvec[k] = thereversion
                 
            else:
                
                for k in range(numactors):
                    rewardvec[k] = calculatereward(thepolicy[k], thesalience[k], poser_pols[windex], poser_pies[windex][k])
            
            poserlist = np.where(posers==1)[0]
            mainstreamlist = np.where(posers==0)[0]
            
            for k in range(len(poserlist)):
                
                pieindexlist[poserlist[k]] = poser_piebuckets[k]
                policyindexlist[poserlist[k]] = poser_policybuckets[k]
            
            for k in range(len(mainstreamlist)):
                
                pieindexlist[mainstreamlist[k]] = -1
                policyindexlist[mainstreamlist[k]] = -1
            
            for k in range(numactors):
                
                if(rewardvec[k] > bestreward[k]):
                    bestreward[k] = rewardvec[k]
                    bestpie[k] = pieindexlist[k]
                    bestpolicy[k] = policyindexlist[k]
                    bestputin[k] = putin_votes[k]
        
        for j in range(numactors):
            if(playerproposeprobs[j][1] == 1):
                choicetoconverge[j] == 1
                
            if(np.any(playerpieprobs[j]) == 1):
                pcpieconverge[j] == 1
                
                if(np.any(playerpolicyprobs[j][np.argmax(playerpieprobs[j])]) == 1):
                    pcpoliconverge[j] == 1
                
            if(playerproposeprobs[j][0] == 1):
                choicetoconverge[j] == 1 
                pcpieconverge[j] == 1                   
                pcpoliconverge[j] == 1

                
            if(bestreward[j] > thereversion ):
                if(bestpie[j] == -1):
                    
                    #if(i > 2000):
                        playerproposeprobs[j] = updateprob(playerproposeprobs[j], learningrate/100*(bestreward[j]/thereversion), 0)
                    
                else:
                    #if(i > 2000):
                    playerproposeprobs[j] = updateprob(playerproposeprobs[j], learningrate/100*(bestreward[j]/thereversion), 1)    
                    playerpieprobs[j] = updateprob(playerpieprobs[j], learningrate*(bestreward[j]/thereversion), bestpie[j])
                    playerpolicyprobs[j][bestpie[j]] = updateprob(playerpolicyprobs[j][bestpie[j]], learningrate*(bestreward[j]/thereversion),  bestpolicy[j])
    
    print(final_pies)
    print(votes)
                














    
    
    
    
    
    