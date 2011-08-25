#import re
#o=open('written.al.pos').read()
#def inflected(word, lemma):
#    
#    r1=re.compile(" %s (v.*) \d+ " % word)
#    pos=r1.findall(o)[0]
#    
#    r2=r=re.compile(" (.*) %s.* \d+ %s\n" % (pos,lemma))
#    inflected_word=r2.findall(o)[0]
#    
#    return inflected_word

import os
ROOT_PATH=os.path.dirname(__file__)


import sqlite3
def inflected(word, lemma, target="v"):
    inflected_word=lemma
    db=sqlite3.connect(os.path.join(ROOT_PATH,"inflect.db"))
    cursor = db.cursor()
    word=word.replace("'","''")
    lemma=lemma.replace("'","''")
    cursor.execute("select * from dic where lemma=='%s' and pos like '%s%%' and substr(pos,3,1) in (select substr(pos,3,1) from dic where word=='%s' and pos like '%s%%' order by freq desc) order by freq desc" %  (lemma,target,word,target))
    #print "select * from dic where lemma=='%s' and pos in (select pos from dic where word=='%s' and pos like '%s%%' order by freq desc)" %  (lemma,word,target)
    r=cursor.fetchall()
    db.close
    if len(r)>0:
        inflected_word=r[0][1]
#    posin=os.popen('egrep " %s %s.*" written.al.pos' % (word, target)).read()
#    posin=posin.split(" ")
#    if len(posin)>=3:
#        pos=posin[2]
#        inflectin=os.popen('egrep "[^\'] %s [0-9]+ %s\r" written.al.pos' % (pos,lemma)).read()
#        
#        if inflectin:
#            s=inflectin.split("\r\n")[:-1]
#            s.sort(key= lambda x: x.split(" ")[0], reverse=True)
#            inflected_word=s[0].split(" ")[1]
    return inflected_word