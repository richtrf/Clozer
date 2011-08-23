#-*- coding: utf8 -*-
import sqlite3 as sqlite
import socket
import sys
import time



def buildDB():
    conn = sqlite.connect('ACL.db3')
    cursor = conn.cursor()
    
    cursor.execute('create table ACL_sentence(sent_id int, sentence varchar)')
    cursor.execute('create index ACL_sentence_sent_id on ACL_sentence(sent_id)')
    #store the tokenized & POS result
    cursor.execute('create table ACL_WP(sent_id int, sentence varchar)')
    cursor.execute('create index ACL_WP_sent_id on ACL_WP(sent_id)')    
    #store the parse tree
    cursor.execute('create table ACL_Tree(sent_id int, Tree varchar)')
    cursor.execute('create index ACL_Tree_sent_id on ACL_Tree(sent_id)')    
    #store the dependency
    cursor.execute('create table ACL_Dep(sent_id int, Dep varchar)')
    cursor.execute('create index ACL_Dep_sent_id on ACL_Dep(sent_id)')     
    
    Datas = [data.strip() for data in open('/home/wujc/workspace/corpus/ACL_S','r').readlines()]
    for i in range(len(Datas)):
        try:

            cursor.execute("insert into ACL_sentence values (%d,'%s')" % (i,Datas[i].strip().decode('utf').encode('utf8').replace("'","''")))
        except:
            print "..",Datas[i],".."

        if i % 10000 == 1:
            conn.commit()
            print i
    
    conn.commit()

def getParsing(data):
    #create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost' #'140.114.75.30' #sys.argv[1] # server address
    #host = '10.185.230.23'
    port = 4444 #int(sys.argv[2]) # server port
    s.connect((host, port))
    s.send(data+"\n  \n\n")
    i = 0
    output = ""
    while(1):
        data = s.recv(1000000) # read up to 1000000 bytes
        i += 1
        if (i < 500): # look only at the first part of the message
            #print data
            output += data
        if not data: # if end of data, leave loop
            break
    #print output
    # close the connection
    s.close()
    return output

def parsing_sentence(min_no = 20,max_no = 25,group_no = 1):
    jump_list = [467699,454436,139078,3357, 81051,16479,106808, 324056, 407646, 407676, 407677,419286, 6879,17855]
    conn = sqlite.connect('ACL.db3')
    cursor = conn.cursor()
    #get the done list
    print 'loading done list',time.ctime()
    Done_Dic = dict([(data[0],1) for data in cursor.execute('select sent_id from ACL_WP').fetchall()])
    print 'loading wait for done list',time.ctime()
    sentences = [data for data in cursor.execute('select * from ACL_sentence where sent_id > 484797').fetchall() if data[0] not in Done_Dic and data[1].count(" ")>= min_no and data[1].count(" ")<max_no and data[0] not in jump_list]
    #一次送一組  比較省時間
    group_i = 0
    print 'starting ...',time.ctime()
    sentence_group = sentences[group_i*group_no:(group_i+1)*group_no]
    print sentence_group
    while len(sentence_group) > 0:
        query = "\n".join([data[1].encode('utf8') for data in sentence_group])+"\n \n\n"
        #print query
        #print 'sending query',time.ctime()
        ParsingResult = getParsing(query).replace("\r","").split("\n\n") #tokenization, tree, dep
        #print 'Get group %d parsing result' % group_i,time.ctime()
##        print len(ParsingResult)
##        for data in ParsingResult:
##            print data
##            print "="*30
            
        for i in range(0,len(ParsingResult),3)[:-1]:
            cursor.execute("insert into ACL_WP values (%d,'%s')" % (sentence_group[i/3][0],ParsingResult[i].replace("'","''")))
            cursor.execute("insert into ACL_Tree values (%d,'%s')" % (sentence_group[i/3][0],ParsingResult[i+1].replace("'","''")))
            cursor.execute("insert into ACL_Dep values (%d,'%s')" % (sentence_group[i/3][0],ParsingResult[i+2].replace("'","''")))
            conn.commit()
        print "Group %d parsing OK" % group_i, time.ctime()         
        group_i += 1
        sentence_group = sentences[group_i*group_no:(group_i+1)*group_no]
        print sentence_group        
    conn.commit()                                
    conn.close()

#buildDB()
#parsing_sentence()
