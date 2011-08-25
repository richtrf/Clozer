import sqlite3

import os
ROOT_PATH=os.path.dirname(__file__)

def vncheck(v,n):
    db=sqlite3.connect(os.path.join(ROOT_PATH,"VNCo_list.db"))
    cursor = db.cursor()
    v=v.replace("'","''")
    n=n.replace("'","''")
    cursor.execute("SELECT * FROM t1 WHERE v=='%s' and n=='%s' and source=='vn'" % (v,n) )
    r=cursor.fetchall()
    db.close
    return r

def allV(n):
    db=sqlite3.connect(os.path.join(ROOT_PATH,"VNCo_list.db"))
    cursor = db.cursor()
    n=n.replace("'","''")
    cursor.execute("SELECT * FROM t1 WHERE n=='%s'" % (n))
    r=cursor.fetchall()
    db.close
    return [i[5] for i in r]