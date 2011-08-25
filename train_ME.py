# -*- coding: UTF-8 -*-

import MontyLemmatiser as m
mst=m.MontyLemmatiser()
import MontyTokenizer as s
sst=s.MontyTokenizer()


import re
regexW = re.compile("\s\(([^ (]+) ([^\)\(]*|\([^\s\(\)]+\))\)")
regexR = re.compile("(.+)\(([^ (]+), ([^\(\)]+)\)")
regexT = re.compile('(.+)-(\d+)')
regexS = regexS = re.compile('([^\s]*)/([^\s]+)')

def SenSplit(linein):
    return linein.split("(ROOT")[1:]
def RegWord(linein):
    return regexW.findall(linein)
def RegRel(linein):
    return regexR.findall(linein)
def RegRel_stanford_online(linein):
	return [(i1.strip(),i2.strip(),i3.strip()) for i1,i2,i3 in regexR.findall(linein.replace(')',')\n'))]

def RegToken(linein):
    return [(i[0],int(i[1])) for i in regexT.findall(linein)][0]
def RegS(linein):
    return regexS.findall(linein)
def stem(wordin):
    return mst.lemmatise_word(wordin)
def ssplit(datain):
    w=[]
    for i in sst.split_sentences(datain):
        w.append(i)
#        for x in i.split(";"): 
#            for y in x.split(","):
#                w.append(y)
    return w

def Ffeed(entry):
    ME_seed=[]
    for i in entry["RELATION"]:
        if i[0]=='dobj':
            v, vno = RegToken(i[1]) #AN
            n, nno = RegToken(i[2]) #AN
            text=[j[1] for j in entry["TEXT"]]
            vindex=int(vno)-1
            nindex=int(nno)-1
            
            feature=[]
            
            if vncheck(v,n): #AN
                feature.append("CN="+stem(n).lower())
                if (vindex-2)>=0:
                    feature.append("CX1="+stem(text[vindex-2]).lower())
                if (vindex-1)>=0:
                    feature.append("CX1="+stem(text[vindex-1]).lower())
                if (vindex+1)<=len(text)-1 and (vindex+1)<>nindex:
                    feature.append("CX2="+stem(text[vindex+1]).lower())
                if (vindex+2)<=len(text)-1 and (vindex+2)<>nindex:
                    feature.append("CX2="+stem(text[vindex+2]).lower())
                ME_seed.append((feature,stem(v).lower()))            
    return ME_seed

def dic_compile(filein):
    fh=open(filein)
    p=fh.read().split('(ROOT\n  (NP (NN XXXXX) (. .)))')
    dic=[]        
    for i in range(0, len(p)):
        s=SenSplit(p[i])
        for j in range(0, len(s)):
            dic.append({"PNO":i+1,"SNO":j+1,"TEXT":RegWord(s[j]),"RELATION":RegRel(s[j])})
    return dic
        


            
if __name__ == '__main__':

    ## KEY modules
    from vnco import vncheck, ancheck
    from random_split import ran
    from HTML_show import show_table
    import maxent
    
    import os
    os.chdir("./monty")
    import MontyLemmatiser as m
    mst=m.MontyLemmatiser()
    os.chdir("..")

    
    
    
    
    data=dic_compile("c_in.out")
    data_dobj=[i for i in data if "dobj" in [j[0] for j in i["RELATION"]]]
    
    ## RANDOM SPLIT
    x2,x1 = ran(data_dobj, 600, "2")

    maxent.set_verbose(1)
    m=maxent.MaxentModel()
    
    m.begin_add_event()
    for i in x1:
        for j1, j2 in Ffeed(i):
                m.add_event(j1, j2, 1)
    
    m.end_add_event()
    m.train()
    m.save("model_2009-11-11_split")
  
  
    ## TEST ON SEPARATE EXPERT DATA
    candi_rank=[]
    candi_false=[]
    for i in x2:
        text=" ".join([o[1] for o in i['TEXT']])
        for j1, j2 in Ffeed(i):
            candi=[k[0] for k in m.eval_all(j1)[:30]]
            if j2 in candi:
                rank=candi.index(j2)+1
                candi_rank.append((rank, j2, candi, j1, text))
            else:
                candi_false.append((99, j2, candi, j1, text))
  
    
    
    ## SHOW RESULT
    show_table(candi_rank+candi_false,'result.html')
    print "COVERAGE:", len(candi_rank)*100.00/len(candi_rank+candi_false)
    print "MRR:", sum([1.00/i[0] for i in candi_rank if i[0]<=10])*1.00/len(candi_rank+candi_false)
  
  
  
  
  
  
          
