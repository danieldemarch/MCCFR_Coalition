#from rulesgen import *
from calculationutils import *
from aiproposalgeneration import *
from playertreegeneration import *
from learninglooputils import *
import numpy as np

megalist = []
megalist2 = []

numactors = 10
numpolicies = 5
thereversion = 0.1
nbiggest = 2
numdivisions = 12
learningrate = 0.2
numiter = 1
    
thepower = np.array([31,30,24, 21, 15, 10, 10, 5, 2, 2])
    
thepolicy = np.array([[.8545455, .3454545, .8545455, .6, .8454545],
                              [.3454545, .3, .4545454, .55, .5181818],
                              [.55, .47, .8100001, .625, 1],
                              [.6090909, .5909091, .7, .575, .7],
                              [.1272727, .3909091, .5363637, .475, .6],
                              [.5909091, .0909091, .3818182, .34, .3363636],
                              [.2818182, .1363636, .1545455, .45, .2636364],
                              [.44, .6363636, .4666666, .45, .49],
                              [.6625, .96, .65, .475, .8125],
                              [.4166667, .28, .1625, .5, .35]])
    
thepolicy = np.rint(thepolicy)
        
thesalience = np.array([[.2609344, .2017893, .1426441, .1093439, .2852882],
                                [.2640827, .1989664, .1844961, .1136951, .2387597],
                                [.1768612, .2268438, .099965, .1153443, .3809857],
                                [.2222222, .2222222, .1647509, .1264368, .2643678],
                                [.3234515, .1719018, .1490058, .1085094, .2471315],
                                [.2023121, .2365496, .1991996, .156514, .2054246],
                                [.1973075, .2179217, .2856542, .101809, .1973075],
                                [.1901798, .2662517, .197787, .1521439, .1936376],
                                [.1544652, .3311916, .1431075, .1577103, .2135255],
                                [.0973631, .2068966, .4198783, .1460446, .1298175]])
    
    
"""
    thepower = np.array([31,30,24, 21, 15, 10, 10, 5, 2, 2])
    
    thepolicy = np.array([[.8545455, .3454545, .8545455, .6, .8454545],
                              [.3454545, .3, .4545454, .55, .5181818],
                              [.55, .47, .8100001, .625, 1],
                              [.6090909, .5909091, .7, .575, .7],
                              [.1272727, .3909091, .5363637, .475, .6],
                              [.5909091, .0909091, .3818182, .34, .3363636],
                              [.2818182, .1363636, .1545455, .45, .2636364],
                              [.44, .6363636, .4666666, .45, .49],
                              [.6625, .96, .65, .475, .8125],
                              [.4166667, .28, .1625, .5, .35]])
        
    thepolicy = np.rint(thepolicy)
        
    thesalience = np.array([[.2609344, .2017893, .1426441, .1093439, .2852882],
                                [.2640827, .1989664, .1844961, .1136951, .2387597],
                                [.1768612, .2268438, .099965, .1153443, .3809857],
                                [.2222222, .2222222, .1647509, .1264368, .2643678],
                                [.3234515, .1719018, .1490058, .1085094, .2471315],
                                [.2023121, .2365496, .1991996, .156514, .2054246],
                                [.1973075, .2179217, .2856542, .101809, .1973075],
                                [.1901798, .2662517, .197787, .1521439, .1936376],
                                [.1544652, .3311916, .1431075, .1577103, .2135255],
                                [.0973631, .2068966, .4198783, .1460446, .1298175]])
"""
    
thepowercombo, powertest = makepowercombinations(thepower)
thecoalition = makeallpossiblecoalitions(thepowercombo, powertest)
    
thepies = makepossiblepieslices(numactors, numdivisions)
    
playerpies = makeplayerpies(thepies)
    
aipiechoices, aipolchoices = find_minimal_coalitions_for_each(thecoalition, thepower, thepolicy, thepies, nbiggest, thereversion, thesalience)
    

for z in range(numiter):

    aiprobabilityvector = returnflatprobability(aipiechoices)
    
    aicoalitionprobs = returnflatprobability(np.zeros(2))
            
    #generate possible pie divisions and prob vectors and append to appropriate lists
    #wait fuck
    #pie should map to coalition, then policy maps to coalition and pie.
    #or... could try mapping both to coalition and see how do.
    #try it with the simple do and see if it converges to the optimum solution.
    
    playerpieprobs = returnflatprobability(playerpies)
    
    #generate all policy strings of length (numpolicies) to give the possible policies to propose
    thepossiblepolicies = returnallpolicystrings(numpolicies)
    
    #generate a single prob vector for coalitions and (numcoalitions) prob vectors for policies
    #wait... policy probs should be based off coalition choice, no?
    #since weighting equal i'm guessing it'll converge just the same.
    playerpolicyprobs = np.full((len(thepies), numpolicies), 1/numpolicies)
    
    ticker = 0
    
    choiceconverge = -1
    
    aicoalconverge = -1
    
    pccoalconverge = -1
    
    pcpieconverge= -1
    
    pcpoliconverge = -1
    
    convergedtoaiprop = 0
    convergedtoplayerprop = 0
    i = 0
    
    runningsumofaichoices = np.zeros((nbiggest, numactors))
    
    besteverreward = 0
    
    while(convergedtoaiprop == 0 and convergedtoplayerprop == 0):
        if(aicoalconverge != -1):
            convergedtoaiprop = 1
        
        if(pcpieconverge != -1 and pcpoliconverge != -1):
            convergedtoplayerprop = 1
        
        if(i%10 == 0):
            print(i, np.max(playerpieprobs), np.argmax(playerpieprobs))
        i+=1
        
        pieresults = 0
        polresults = 0
        playerreward = 0
        bestreward = 0
        coalresults = 0
        bestpie = 0
        bestpol = 0
        
        #pick random ai coalitions/policies and then evaluate, adding to running sum
        
        aipies = np.zeros((nbiggest, numactors))
        aipolicies = np.zeros((nbiggest, numpolicies))
                
        for j in range(nbiggest):
            choice = np.random.randint(0, len(aipiechoices))
            
            aipies[j] = aipiechoices[j][choice]
            aipolicies[j] = aipolchoices[j][choice][0]
            
            for k in range(numactors):
            
                runningsumofaichoices[j, k]+=calculatereward(thepolicy[k], thesalience[k], aipolchoices[j][choice], aipiechoices[j][choice][k]) 
        
        #do some iters of player creating their own coalition
        for z in range(5000):
            ticker+=1
                    
            pieresults, polresults, playerreward = playercreatespath(coalresults, pieresults, polresults, playerreward, aipies, aipolicies, playerpies, playerpieprobs, thepossiblepolicies, playerpolicyprobs, thereversion, thepolicy, thesalience, thepower)
                    
            if(playerreward > bestreward):
                bestreward = playerreward
                bestpie = pieresults
                bestpol = polresults
                bestbucket = 1
        #print("power to beat", powtobeat)
        #print("total votes", votes)
        #print("player's reward", playerreward)
    
        playerpieprobs = updateprob(playerpieprobs, learningrate, bestpie)
                                
        playerpolicyprobs[bestpie] = updateprob(playerpolicyprobs[bestpie], learningrate/10, bestpol)
    
        if(np.any(playerpieprobs == 1) and pcpieconverge == -1):
                pcpieconverge = i
                print("pie converged", i)
    
        if(np.any(playerpolicyprobs[bestpie] == 1) and pcpoliconverge == -1):
                pcpoliconverge = i
                print("policy converged", i)
         
    bestpieindex = np.argmax(playerpieprobs)
    bestpie = playerpies[bestpieindex]
    
    print("optimal pie", bestpie)
    
    bestpolindex = np.argmax(playerpolicyprobs[bestpieindex])
    
    bestpol = thepossiblepolicies[bestpolindex]
    
    print("optimal policy", bestpol)
    
    rewardvec = np.zeros((numactors))
    
    for k in range(numactors):
        rewardvec[k] = calculatereward(thepolicy[k], thesalience[k], bestpol, bestpie[k])
    
    print("reward for these for all players", rewardvec)
    
    for k in range(nbiggest):
        print("reward for player", k+1, "'s average policy", runningsumofaichoices[k]/i)
        
    megalist.append(bestpie)
    megalist2.append(bestpol)
    
    
megalist = np.array(megalist)
for i in range(len(megalist)):
    listydo = []
    for j in range(len(megalist[i])):
        if(megalist[i][j]>0):
            listydo.append(j)
    print(listydo)
    
    
    
    
    
    
    
    
    
    
    