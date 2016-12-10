'''
Created on 8/10/2015

@author: Sam Hunt
'''

import pylab as pl
import datetime

from findLmers import slidingLmerCountUpTo 
from findLmers import dpTreeLmerCountUpTo
from findLmers import dpTreeLmerCountUpTo2

def plot_complexity_comparison(db,L,filename):
    
    x,y=[],[]
    for i in range(1,L+1):
        start = datetime.datetime.now()
        slidingLmerCountUpTo(db, i)
        time = (datetime.datetime.now()-start).total_seconds()
        print (time)
        x.append(i)
        y.append(time)
        pl.annotate(s=truncate(time, 1),xy=(i,time+2))
    sliding = pl.scatter(x,y, marker='o',color='blue')
    print()
    
    x,y=[],[]
    for i in range(1,L+1):
        start = datetime.datetime.now()
        dpTreeLmerCountUpTo(db, i)
        time = (datetime.datetime.now()-start).total_seconds()
        print (time)
        x.append(i)
        y.append(time)
        pl.annotate(s=truncate(time, 1),xy=(i,time+2))
    dptree = pl.scatter(x,y, marker='o',color='red')
    print()
    
    x,y=[],[]
    for i in range(1,L+1):
        start = datetime.datetime.now()
        dpTreeLmerCountUpTo2(db, i)
        time = (datetime.datetime.now()-start).total_seconds()
        print (time)
        x.append(i)
        y.append(time)
        pl.annotate(s=truncate(time, 1),xy=(i,time+2))
    dptree2 = pl.scatter(x,y, marker='o',color='green')
    print()
    
    pl.legend((sliding,dptree, dptree2),('sliding','dptree', 'dptree2'),loc='upper left', scatterpoints=1)
    pl.xlim(xmin=0,xmax=L+1)
    pl.ylim(ymin=0)
    pl.title("Sliding vs DPTree Lmer-finding algorithm runtime complexities")
    pl.xlabel("Maximum Lmer length (L)")
    pl.ylabel("Algorithm runtime (seconds)")
    pl.savefig(filename)
    pl.show()

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, _, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])
