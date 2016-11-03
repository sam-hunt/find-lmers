'''
Created on 6/10/2015

@author: Sam Hunt
'''

from itertools import product

import plotLmerFinderComplexities

def lmers(l):
    return list(''.join(i) for i in product("ACGT",repeat=l))

def lmersUpTo(l):
    allLmers = []
    for i in range(1,l+1):
        allLmers.extend(lmers(i))
    return allLmers

def loadDB(filename):    
    with open(filename,'r') as f:
        db = ''.join(f.read().split())
    return db
    
def slidingLmerCount(db,l):
    counts = {}
    for i in range(len(db)-l+1):
        lmer=db[i:i+l] 
        if lmer in counts.keys():
            counts[lmer] += 1
        else:
            counts[lmer] = 1
    return counts

def slidingLmerCountUpTo(db,l):
    allLCounts = {}
    for i in range(1,l+1):
        allLCounts.update(slidingLmerCount(db, i))
    return allLCounts

def slidingLmerCountUpToSaveToFile(db,l,filename):
    with open(filename,"w") as f:
        for k,v in slidingLmerCount(db, 1).items():
            f.write(str(k) + " " + str(v)+ "\n")
    for i in range(1,l+1):
        with open(filename,"a") as f:
            for k,v in slidingLmerCount(db, i).items():
                f.write(str(k) + " " + str(v)+ "\n")

def dpTreeLmerCountUpTo(db,l):
    lmerCount = {'A':0,'C':0,'G':0,'T':0}
    lmerPositions = {'A':[],'C':[],'G':[],'T':[]}
    
    for i in range(len(db)):
        j = db[i]
        lmerCount[j] += 1
        lmerPositions.get(j).append(i)
    
    for i in range(2,l+1):                                      #for each length Lmer
        for j in lmers(i):                                      #for each Lmer of a given length
            if j[:-1] in lmerCount.keys():                      #only check for descendant Lmers if a parent exists
                pp = lmerPositions[j[:-1]]                      #get the possible positions of an Lmer based on its parent's positions
                for epp in pp:                                  #for each possible position of a descendant Lmer
                    try:
                        if db[epp+i-1] == j[-1]:                #see if the Lmer is actually there
                            if j in lmerCount.keys():           #if it is there, and we have seen it before,
                                lmerCount[j] += 1               #increment the Lmer count for it 
                                lmerPositions[j].append(epp)    #and add its position to the known positions for descendants to check against
                            else:
                                lmerCount[j] = 1                #otherwise just add it as a new key
                                lmerPositions[j] = [epp]
                    except IndexError:                          #we'll hit some of these at end of file
                        pass       
                        
    return lmerCount

def dpTreeLmerCountUpTo2(db,l):                                 #reduces memory consumption by only tracking 2 generations of positions instead of all
    lmerCount = {'A':0,'C':0,'G':0,'T':0}
    lmerLastPositions = {'A':[],'C':[],'G':[],'T':[]}
    lmerCurrPositions = {}
    
    for i in range(len(db)):
        j = db[i]
        lmerCount[j] += 1
        lmerLastPositions.get(j).append(i)
    
    for i in range(2,l+1):                                      #for each length Lmer
        for j in lmers(i):                                      #for each Lmer of a given length
            k = j[:-1] 
            if k in lmerCount.keys():                           #only check for descendant Lmers if a parent exists
                pp = lmerLastPositions[k]                       #get the possible positions of an Lmer based on its parent's positions
                for epp in pp:                                  #for each possible position of a descendant Lmer
                    try:
                        if db[epp+i-1] == j[-1]:                #see if the Lmer is actually there
                            if j in lmerCount.keys():           #if it is there, and we have seen it before,
                                lmerCount[j] += 1               #increment the Lmer count for it 
                                lmerCurrPositions[j].append(epp)    #and add its position to the known positions for descendants to check against
                            else:
                                lmerCount[j] = 1                #otherwise just add it as a new key
                                lmerCurrPositions[j] = [epp]
                    except IndexError:                          #we'll hit some of these at end of file
                        pass       
        lmerLastPositions = lmerCurrPositions
        lmerCurrPositions = {}
    return lmerCount



if __name__ == '__main__':
    
    ll = lmersUpTo(2)
    print (len(ll), ll)
    
    db = loadDB('../res/ecoli.txt')
    print (len(db))
    
    plotLmerFinderComplexities.plot_complexity_comparison(db, 10, '../out/SlidingVsTreeAlgorithmRuntimes7.png')
    
    #start = datetime.datetime.now()
    #dp = dpTreeLmerCountUpTo(db, 7)
    #print len(dp), sorted(dp.iteritems())
    #print (datetime.datetime.now()-start)
    
     
    #start = datetime.datetime.now()
    #ss = slidingLmerCountUpTo(db, 7)
    #slidingLmerCountUpToSaveToFile(db,10,"Ecoli_10mers.txt")
    
    #print len(ss), sorted(ss.iteritems())
    #print set(ss.keys())-set(dp.keys())
    #print (datetime.datetime.now()-start)
    
    
    


