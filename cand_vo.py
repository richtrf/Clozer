import sqlite3

import os
ROOT_PATH=os.path.dirname(__file__)

def vo(v,n=1):
    db=sqlite3.connect(os.path.join(ROOT_PATH,"vo.db"))
    cursor = db.cursor()
    v=v.replace("'","''")
    
    cursor.execute("SELECT w2 FROM sim WHERE w1=='%s'" % (v) )
    r=cursor.fetchall()
    candi=set([i[0] for i in r])
    
    for i in range(n-1):
        vlist=candi
        for x in list(vlist):
            cursor.execute("SELECT * FROM sim WHERE w1=='%s'" % (x) )
            r=cursor.fetchall()
            for j in r:
                candi=candi.union(j)
    
    db.close
    return candi


#import csv
#
## Building volist from verbocean raw data
#volist={}
#for row in csv.reader(open('silost.csv')):
#    w1,w2=row[:2]
#    if w1 in volist:
#        volist[w1].append(w2)
#    else:
#        volist[w1]=[w2]
#
## Generate the verb candidates via verbocean
#def vo_cand(word_in,n=1):
#    v=set()
#    try:   
#        v=set(volist[word_in])  # Initial: the 0-word-in-between relationship
#        for i in range(n-1):    # range(0) implies this wont fuction
#            for x in v:
#                v=v.union(volist[x])
#    finally: 
#        return v
