#from rulesgen import *
from calculationutils import *
from aiproposalgeneration import *
from playertreegeneration import *
from learninglooputils import *
from getcasedata import *
import numpy as np

megalist = []
megalist2 = []

case = 'AUT_1999_1_PPMD'

if(case=='AUT_1999_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = AUT_1999_1_PPMD()

if(case=='BEL_2003_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = BEL_2003_1_PPMD()
    
if(case=='BUL_2001_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = BUL_2001_1_PPMD()
    
if(case=='cz_2006_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = cz_2006_1_CHES()

if(case=='DEU_2002_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = DEU_2002_1_PPMD()
        
if(case=='DNK_2005_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = DNK_2005_1_CHES()

if(case=='est_2007_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = est_2007_1_CHES()

if(case=='FIN_1999_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = FIN_1999_1_PPMD()

if(case=='hun_2002_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = hun_2002_1_PPMD()

if(case=='lat_2006_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = lat_2006_1_CHES()

if(case=='LUX_2009_1_JOP'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = LUX_2009_1_JOP()

if(case=='NLD_2010_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = NLD_2010_1_CHES()

if(case=='pol_2007_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = pol_2007_1_CHES()

if(case=='PRT_1999_1_PPMD'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = PRT_1999_1_PPMD()

if(case=='ROM_2008_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = ROM_2008_1_CHES()

if(case=='slovak_2010_1_CH'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = slovak_2010_1_CH()

if(case=='sloven_2000_1_PP'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = sloven_2000_1_PP()

if(case=='SPA_2008_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = SPA_2008_1_CHES()

if(case=='SWE_2006_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = SWE_2006_1_CHES()

if(case=='uk_2010_1_CHES'):
    numactors, numpolicies, thepower, thepolicy, thesalience, learningrate, thereversion, nbiggest, numdivisions = uk_2010_1_CHES()

player = 1

if(player == 1):
    temppow = thepower[0].copy()
    temppol = thepolicy[0].copy()
    tempsal = thesalience[0].copy()
    
    thepower[0] = thepower[1]
    thepolicy[0] = thepolicy[1]
    thesalience[0] = thesalience[1]
    
    thepower[1] = temppow
    thepolicy[1] = temppol
    thesalience[1] = tempsal
    

numsearches = 10000
numiter = 20
thereversion = 0.4/numactors
#learningrate = 0.1
    
thepowercombo, powertest = makepowercombinations(thepower)
thecoalition = makeallpossiblecoalitions(thepowercombo, powertest)
    
thepies = makepossiblepieslices(numactors, numdivisions)
    
playerpies = makeplayerpies(thepies)
    
aipiechoices, aipolchoices = find_minimal_coalitions_for_each(thecoalition, thepower, thepolicy, thepies, nbiggest, thereversion, thesalience)

#generate all policy strings of length (numpolicies) to give the possible policies to propose
thepossiblepolicies = returnallpolicystrings(numpolicies)

for z in range(numiter):

    aiprobabilityvector = returnflatprobability(aipiechoices)
    
    aicoalitionprobs = returnflatprobability(np.zeros(2))
            
    #generate possible pie divisions and prob vectors and append to appropriate lists
    #wait fuck
    #pie should map to coalition, then policy maps to coalition and pie.
    #or... could try mapping both to coalition and see how do.
    #try it with the simple do and see if it converges to the optimum solution.
    
    playerpieprobs = returnflatprobability(playerpies)
    
    #generate a single prob vector for coalitions and (numcoalitions) prob vectors for policies
    #wait... policy probs should be based off coalition choice, no?
    #since weighting equal i'm guessing it'll converge just the same.
    playerpolicyprobs = np.full((len(playerpies), len(thepossiblepolicies)), 1/len(thepossiblepolicies))
    
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
            piemaxindex = np.argmax(playerpieprobs)
            polmaxindex = np.argmax(playerpolicyprobs[piemaxindex])
            print(i, np.max(playerpieprobs), piemaxindex, playerpies[piemaxindex], np.max(playerpolicyprobs), polmaxindex, thepossiblepolicies[polmaxindex])
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
            
            choice = np.random.randint(0, len(aipiechoices[j]))
            
            aipies[j] = aipiechoices[j][choice]
            aipolicies[j] = aipolchoices[j][choice]
            
            for k in range(numactors):
                
                runningsumofaichoices[j, k]+=calculatereward(thepolicy[k], thesalience[k], aipolchoices[j][choice], aipiechoices[j][choice][k]) 
        
        #do some iters of player creating their own coalition
        for z in range(numsearches):
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
    
        playerpieprobs = updateprob(playerpieprobs, learningrate/10, bestpie)
                                
        playerpolicyprobs[bestpie] = updateprob(playerpolicyprobs[bestpie], learningrate, bestpol)
    
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
finallist = []
for i in range(len(megalist)):
    listydo = []
    for j in range(len(megalist[i])):
        if(megalist[i][j]>0):
            listydo.append(j)
    finallist.append(listydo)
unique, counts = np.unique(np.array(finallist), return_counts = True, axis = 0)
for j in range(len(unique)):
    print(unique[j], counts[j])
        
    
    
    
    
    
    
    