#file to generate and select ai proposals
import numpy as np
import random
import math
from calculationutils import *
from playertreegeneration import *
from numba import jit

def find_minimal_coalitions_for_each(thecoalition, thepower, thepolicy, thepies, nbiggest, thereversion, thesalience):
    nbiggestpies = []
    nbiggestpols = []
    
    theminimalcoalition = []
    
    """
    for i in range(len(nbiggest)):
        
        nbiggestpies.append([])
        nbiggestpols.append([])
    """
    for i in range(len(thecoalition)):
        coalpower = thepower[thecoalition[i]]
        if((np.sum(coalpower)-coalpower[np.argmin(coalpower)]) <= np.sum(thepower)/2 and np.sum(coalpower) > np.sum(thepower)/2):
            theminimalcoalition.append(thecoalition[i])
                
    for i in range(len(theminimalcoalition)):
        
        pie = np.zeros((len(thepower)))
        
        poli = np.zeros((len(thepolicy[0])))
        
        coalpower = np.sum(thepower[theminimalcoalition[i]])
        
        for j in range(len(theminimalcoalition[i])):
            
            pie[theminimalcoalition[i][j]] = thepower[theminimalcoalition[i][j]]/coalpower
            
            poli+=pie[theminimalcoalition[i][j]]*thepolicy[theminimalcoalition[i][j]]
            
            poli = np.rint(poli)
        
        nbiggestpies.append(pie)
        nbiggestpols.append(poli)
        
    rewardfulpies = []
    reweardfulpols = []
    for i in range(len(nbiggestpies)):
        bettertogether=1
        for j in range(len(nbiggestpies[i])):
            if(nbiggestpies[i][j] > 0):
                reward = calculatereward(thepolicy[j], thesalience[j], nbiggestpols[i], nbiggestpies[i][j])
                if(reward<thereversion):
                    bettertogether=0
        if(bettertogether==1):
            reweardfulpols.append(nbiggestpols[i])
            rewardfulpies.append(nbiggestpies[i])
                    
        
    finalpies = []
    finalpols = []
    for i in range(1,nbiggest+1):
        this_little_pie = []
        this_little_pol = []
        for j in range(len(rewardfulpies)):
            if(rewardfulpies[j][i] > 0):
                this_little_pie.append(rewardfulpies[j])
                this_little_pol.append(reweardfulpols[j])
        finalpies.append(this_little_pie)
        finalpols.append(this_little_pol)
        
    return finalpies, finalpols
        

                        
                            
                    
                        
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    
    
    
    