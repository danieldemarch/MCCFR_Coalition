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
    
    #init empty list for the coalitions
    
    theminimalcoalition = []
    
    #check all coalitions to see if they are minimum winning coalitions, if so append them
    
    for i in range(len(thecoalition)):
        coalpower = thepower[thecoalition[i]]
        if((np.sum(coalpower)-coalpower[np.argmin(coalpower)]) <= np.sum(thepower)/2 and np.sum(coalpower) > np.sum(thepower)/2):
            theminimalcoalition.append(thecoalition[i])
                
    for i in range(len(theminimalcoalition)):
        
        pie = np.zeros((len(thepower)))
        
        poli = np.zeros((len(thepolicy[0])))
        arfor = np.zeros((len(thepolicy[0])))
        aragainst = np.zeros((len(thepolicy[0])))
        
        coalpower = np.sum(thepower[theminimalcoalition[i]])
        
        for j in range(len(theminimalcoalition[i])):
            
            #incrememt pie for the coal IFF they are a member
            
            pie[theminimalcoalition[i][j]] = thepower[theminimalcoalition[i][j]]/coalpower
            
            #poli+=pie[theminimalcoalition[i][j]]*thepolicy[theminimalcoalition[i][j]]
            
        for j in range(len(poli)):
            rfor = 0
            ragainst = 0
            for k in range(len(pie)):
                if(pie[k] > 0 and thepolicy[k][j] == 0):
                    ragainst+=thesalience[k][j]
                if(pie[k] > 0 and thepolicy[k][j] == 1):
                    rfor+=thesalience[k][j]
            if(rfor > ragainst):
                poli[j] = 1
            arfor[j] = rfor
            aragainst[j] = ragainst
        
        # print('arfor')
        # print(arfor)
        # print('aragainst')
        # print(aragainst)
        # print('poli')
        # print(poli)
        # print('pie')
        # print(pie)
        
        poli = np.rint(poli)
        nbiggestpies.append(pie)
        nbiggestpols.append(poli)
        
    rewardfulpies = []
    rewardfulpols = []
    for i in range(len(nbiggestpies)):
        bettertogether=1
        for j in range(len(nbiggestpies[i])):
            if(nbiggestpies[i][j] > 0):
                reward = calculatereward(thepolicy[j], thesalience[j], nbiggestpols[i], nbiggestpies[i][j])
                if(reward<thereversion):
                    bettertogether=0
        if(bettertogether==1):
            rewardfulpols.append(nbiggestpols[i])
            rewardfulpies.append(nbiggestpies[i])
                    
    finalpies = []
    finalpols = []
    
    for i in range(1,nbiggest+1):
        this_little_pie = []
        this_little_pol = []
        for j in range(len(rewardfulpies)):
            if(rewardfulpies[j][i] > 0):
                this_little_pie.append(rewardfulpies[j])
                this_little_pol.append(rewardfulpols[j])
        #if(len(this_little_pie) == 1):
         #   finalpies.append(this_little_pie[0])
          #  finalpols.append(this_little_pol[0])
        else:
            finalpies.append(this_little_pie)
            finalpols.append(this_little_pol)        
        
    return finalpies, finalpols
        

                        
                            
                    
                        
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
    
    
    
    