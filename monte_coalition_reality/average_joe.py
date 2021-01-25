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
numdivisions = 5
learningrate = 0.2
numiter = 15
num_traversals = 200
num_strategies = 99
 
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

winlist = []

for i in range(len(allplayerpies)):
    allplayerpies[i] = np.array(allplayerpies[i])
    
    if(i==1):
        cond1 = np.logical_and(allplayerpies[i][:,2] > 0, allplayerpies[i][:,3] > 0)
        cond2 = np.logical_and(allplayerpies[i][:,0] == 0, allplayerpies[i][:,4] == 0)
        cond = np.logical_and(cond1, cond2)
        print(np.count_nonzero(cond))
        allplayerpies[i] = allplayerpies[i][cond]
        #make it so that player 1 can only propose variants of 1, 2, 3 and see what happens
    
    np.random.shuffle(allplayerpies[i])
    
thepossiblepolicies = returnallpolicystrings(numpolicies)

thepossibleposers = returnallpolicystrings(numactors)
        
for z in range(numiter):
    
    playerproposeprobs = []
    playerpieprobs = []
    playerpolicyprobs = []
    playerchoiceprobs = []
    
    for i in range(numactors):
        playerproposeprobs.append(np.array([1-(thepower[i]/np.sum(thepower)), (thepower[i]/np.sum(thepower))]))

        #playerproposeprobs.append(returnflatprobability(np.zeros((2))))
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
    
    while(i < 200):
        
        if(i%1 == 0):
            print(i)
            for j in range(numactors):
                print(playerproposeprobs[j][1], np.max(playerpieprobs[j]), np.max(playerpolicyprobs[j]), allplayerpies[j][np.argmax(playerpieprobs[j])])
            
                
                # if(i>0):
                #     print(poser_pies)
                #     print(poser_pols)
                #     print(votes)
        
        i+=1
        
        final_pie_list = []
        final_pol_list = []
        final_putin_list = []
        final_poser_list = []
        
        chickendinner = np.zeros((numactors))
        for j in range(num_traversals):
            
            posers = find_posers(playerproposeprobs)
            
            while(np.count_nonzero(posers) < 2):
                posers = find_posers(playerproposeprobs)
            
            poser_pies, poser_pols, poser_piebuckets, poser_policybuckets = get_poser_coalitions(posers, allplayerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience)
            
            final_pies, final_pols, putin_votes = handle_conglomeration_boogaloo(poser_pies, poser_pols, posers, thepower)
            
            votes = handle_voting(putin_votes, final_pies, final_pols, thereversion, thepolicy, thesalience, thepower)
            
            final_pie_list.append(final_pies)
            final_pol_list.append(final_pols)
            final_putin_list.append(putin_votes)
            final_poser_list.append(posers)
            windex = numactors*3
            for m in range(len(votes)):
                            
                            if(votes[m] >= np.ceil(np.sum(thepower)/2)):
                                windex = m
                                break 
                            
                        
                        
            if(windex == numactors*3):
                            
                chickendinner+=np.zeros((numactors))
            elif(windex == len(final_pies)):
                            
                chickendinner+=np.zeros((numactors))
            else:
                chickendinner+= (final_pies[windex] > 0)
            
        bestpies = np.zeros((numactors)).astype(int)
        bestpols = np.zeros((numactors)).astype(int)
        
        best_rew = np.zeros((numactors))
        
        print("chicken dinner", chickendinner)
        print()

        for j in range(numactors):
            
            if(playerproposeprobs[j][1] > 0):
                for k in range(num_strategies):
                    stratpie, stratpol, stratpiebucket, stratpolicybucket = creationofcoalitions(allplayerpies[j], playerpieprobs[j], thepossiblepolicies, playerpolicyprobs[j], thereversion, thepolicy, thesalience)
                    avgreward = 0.0
                    
                    for l in range(num_traversals):
                        wins = 0
                        final_pies, final_pols, putin_votes, posers = final_pie_list[l].copy(), final_pol_list[l].copy(), final_putin_list[l].copy(), final_poser_list[l].copy()
                        if(putin_votes[j] == -1):
                            proposedex = len(final_pies)
                            final_pies = np.concatenate((final_pies, stratpie.reshape(1, numactors)))
                            final_pols = np.concatenate((final_pies, stratpol.reshape(1, len(thepolicy[0]))))
                            posers[j] = 1
                            final_pies, final_pols, putin_votes = handle_conglomeration_boogaloo(final_pies, final_pols, posers, thepower)
                        else:
                            final_pies[putin_votes[j]] = stratpie
                            final_pols[putin_votes[j]] = stratpol
                        
                        votes = handle_voting(putin_votes, final_pies, final_pols, thereversion, thepolicy, thesalience, thepower)
                        
                        windex = numactors*3
                        for m in range(len(votes)):
                            
                            if(votes[m] >= np.ceil(np.sum(thepower)/2)):
                                windex = m
                                break 
                            
                        
                        
                        if(windex == numactors*3):
                            
                            avgreward+=thereversion
                                
                        elif(windex == len(final_pies)):
                            
                            avgreward+=thereversion
                             
                        else:
                            
                            
                            if(putin_votes[j] == windex):
                                avgreward+= calculatereward(thepolicy[j], thesalience[j], final_pols[windex], final_pies[windex][j])
                            else:
                                avgreward+=thereversion 
                            
                    if(avgreward >= best_rew[j]):
                        best_rew[j] = avgreward
                        bestpols[j] = stratpolicybucket
                        bestpies[j] = stratpiebucket
            avgreward = 0.0
            if(playerproposeprobs[j][0] > 0):
                    for k in range(num_traversals):
                            final_pies, final_pols, putin_votes = final_pie_list[l].copy(), final_pol_list[l].copy(), final_putin_list[l].copy()
                            if(putin_votes[j] != -1):
                                final_pies = np.delete(final_pies, putin_votes[j], axis = 0)
                                final_pols = np.delete(final_pols, putin_votes[j], axis = 0)
                        
                            if(len(final_pies) == 0):
                                avgreward+=thereversion
                            else:
                                votes = handle_voting(putin_votes, final_pies, final_pols, thereversion, thepolicy, thesalience, thepower)
                                
                                windex = numactors*3
                                for m in range(len(votes)):
                                    
                                    if(votes[m] >= np.ceil(np.sum(thepower)/2)):
                                        windex = m
                                        break 
                                
                                
                                if(windex == numactors*3):
                                    
                                    avgreward+=thereversion
                                        
                                elif(windex == len(final_pies)):
                                    
                                    avgreward+=thereversion
                                else:
                                    
                                    avgreward+= calculatereward(thepolicy[j], thesalience[j], final_pols[windex], final_pies[windex][j])
                                    if(calculatereward(thepolicy[j], thesalience[j], final_pols[windex], final_pies[windex][j]) < 0):
                                        print("error")
            if(j < 5):               
                print("best reward for player", j, "for voting", avgreward/num_traversals, "best for proposing", best_rew[j]/num_traversals)
                print()
                rewardvec = np.zeros((numactors))
                bestpropositionpie = allplayerpies[j][bestpies[j]]
                bestpropositionpol = thepossiblepolicies[bestpols[j]]
                
                for m in range(numactors):
                    rewardvec[m] = calculatereward(thepolicy[m], thesalience[m], bestpropositionpol, bestpropositionpie[m])
                
                print("best proposal pie", bestpropositionpie)
                print()
                print("best proposal policy", bestpropositionpol)
                print()
                print("rewards for others", rewardvec)
                print()
            

            if(avgreward > best_rew[j]):
                    best_rew[j] = avgreward
                    
                 
        print("best reward overall", best_rew/num_traversals)
        print()

        for j in range(numactors):
            if(bestpols[j] == -1 and bestpies[j] == -1):
                    
                    playerproposeprobs[j] = updateprob(playerproposeprobs[j], learningrate/20, 0)
                    playerpieprobs[j] = updateprob(playerpieprobs[j], learningrate, bestpies[j])
                    playerpolicyprobs[j][bestpies[j]] = updateprob(playerpolicyprobs[j][bestpies[j]], learningrate,  bestpols[j])
                
            else:
                    playerproposeprobs[j] = updateprob(playerproposeprobs[j], learningrate/20, 1)    
                    playerpieprobs[j] = updateprob(playerpieprobs[j], learningrate, bestpies[j])
                    playerpolicyprobs[j][bestpies[j]] = updateprob(playerpolicyprobs[j][bestpies[j]], learningrate,  bestpols[j])
            
    posers = find_posers(playerproposeprobs)
            
            
    poser_pies, poser_pols, poser_piebuckets, poser_policybuckets = get_poser_coalitions(posers, allplayerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience)
            
    final_pies, final_pols, putin_votes = handle_conglomeration_boogaloo(poser_pies, poser_pols, posers, thepower)
            
    votes = handle_voting(putin_votes, final_pies, final_pols, thereversion, thepolicy, thesalience, thepower)
    windex = numactors*3
    for m in range(len(votes)):
        if(votes[m] >= np.ceil(np.sum(thepower)/2)):
            windex = m
            break 
    
    if(windex == numactors*3):
        winlist.append(-1)
    else:
        winlist.append(final_pies[windex])
                














    
    
    
    
    
    