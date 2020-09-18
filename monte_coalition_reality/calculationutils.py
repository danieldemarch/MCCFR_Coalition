import numpyimport randomimport mathfrom numba import jitdef returnflatprobability(array):    return numpy.full((len(array)), 1/len(array))#updates probability by a learning rate and index#@jit(nopython=True, fastmath=True)def updateprob(probvec, learningrate, index):    tomult = 1+learningrate    othersum = 0        #if would exceed 1, set to 1 and all others to 0    if(probvec[index]*tomult > 1):        probvec = numpy.zeros((len(probvec)))        probvec[index] = 1    else:        #multiply index appropriately and get the sum of the others        probvec[index] = probvec[index]*tomult                    #find what you'd need to divide each non-index member by to return the sum of the probs to 1, and divides appropriately        downtosize = 1-probvec[index]        othersum = numpy.sum(probvec) - probvec[index]                for i in range(len(probvec)):            if (i != index):                probvec[i] = probvec[i]/(othersum/downtosize)        return probvec#calculates reward by matching policies and pie#@jit(nopython=True, fastmath=True)def calculatereward(mypolicies, mysalience, theirpolicies, mypie):        reward = (numpy.sum(mysalience[mypolicies == theirpolicies])+mypie)/2    return reward#checks which probability "bucket" a 0-1 real value falls into, based on probability vectordef checkbucket(probresult, probvec):    if(0 <= probresult <= probvec[0]):        return 0    else:        for i in range(len(probvec)-1):            sum1 = numpy.sum(probvec[0:i+1])            sum2 = numpy.sum(probvec[0:i+2])            if(sum1 < probresult <= sum2):                return i+1    def checkbucket2(probvec):    return numpy.random.choice(numpy.arange(0, len(probvec)), p=probvec)#@jit(nopython=True, fastmath=True)def checkbucket_pie(probvec):    probresult = random.random()    if(0 <= probresult <= probvec[0]):        return 0    else:        sum1 = 0        sum2 = probvec[0]        for i in range(len(probvec)-1):            sum1+=probvec[i]            sum2+=probvec[i+1]            if(probresult >sum1 and probresult <= sum2):                return i+1        return len(probvec)-1#@jit(nopython=True, fastmath=True)def checkbucket_policy(probvec):    probresult = random.random()    if(0 <= probresult <= probvec[0]):        return 0    else:        sum1 = 0        sum2 = probvec[0]        for i in range(len(probvec)-1):            sum1+=probvec[i]            sum2+=probvec[i+1]            if(probresult >sum1 and probresult <= sum2):                return i+1        return len(probvec)-1#@jit(nopython=True, fastmath=True)def checkbucket_proposal(probvec):    probresult = random.random()    if(0 <= probresult <= probvec[0]):        return 0    else:        sum1 = 0        sum2 = probvec[0]        for i in range(len(probvec)-1):            sum1+=probvec[i]            sum2+=probvec[i+1]            if(probresult >sum1 and probresult <= sum2):                return i+1        return len(probvec)-1            def gametreesizecalc(playercoalitionprobs, playerpieprobs, playerpolicyprobs):    total = 0    for i in range(len(playerpolicyprobs)):        for j in range(len(playerpolicyprobs[i])):            pollen = len(playerpolicyprobs[i][j])            total+= pollen                    return total