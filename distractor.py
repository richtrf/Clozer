from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str

#from buildDB import getParsing
from stanford_html import getHTML
from train_ME import RegWord, RegToken, stem, ssplit, RegRel_stanford_online #RegRel
from inflect import inflected
from vnco_db import vncheck
from cand_vo import vo

import os
ROOT_PATH=os.path.dirname(__file__)


import random
import simplejson as json
elist=json.loads(open(os.path.join(ROOT_PATH,'entrance_verb.txt')).read())
hverb=['have', 'do', 'know','think','get', 'go','see','say' ,'come','make','take','look','give','find','use']


def distractor_inflected(vin, n, org, freq=5):
    vList= list(vo(vin,2)) + random.sample(hverb,15)
    dis=[i for i in vList if not vncheck(i,n) and i in elist]
    return sorted([inflected(org,i) for i in dis[:3]]+[org])

def sen_dis(s, starting, f_status="only_VN", m_status="1"):
    
    # TARGET EXTRACTION
    p=getHTML(s)
    target=[(w1,w2) for rel, w1, w2 in RegRel_stanford_online(p) if rel=='dobj' or rel=='nsubjpass']    # active/passive
    
    # MORE OPTIONS
    if f_status=="AN":
        target=target+[(w2,w1) for rel, w1, w2 in RegRel(p) if rel=='amod']
    
    
    # TEXT & BALNK-OUT
    w=[i[1] for i in RegWord(p)]
    blank=[RegToken(v)[1] for v,n in target]
    
    global item_no
    w_blank=[]
    for i in range(0, len(w)):
        o=w[i]
        if i+1 in blank:
            item_no+=1
            o="___%d___" % (item_no)
        w_blank.append(o)
    
    
    # DISTRACTOR
    target_token=[(RegToken(w1)[0], RegToken(w2)[0]) for w1, w2 in target]
    
    nstem=lambda x: x[-1]=='s' and stem(x) or x
    if m_status=="1":     
        dis=[(key, distractor_inflected(stem(key), nstem(noun), key)) for key, noun in target_token]
    else:
        dis=[(key, distractor_inflected_etds(stem(key), nstem(noun), key)) for key, noun in target_token]
    
    
    key_dis=[]
    for key, dis_item in dis:
        starting+=1
        random.shuffle(dis_item)
        key_dis.append([starting, "(1) %s (2) %s (3) %s (4) %s" % tuple(dis_item), dis_item.index(key)+1,dis_item])
    
    return w_blank, key_dis 



 
def index(request):

    global item_no
    item_no=0
    r=request.POST
    
#    <input type="checkbox" name="f_status" value="AN"> AN collocation
#    f_status="only_VN"
    
#    if 'f_status' in r:
#        f_status = smart_str(r['f_status'])
#    
#    m_status ="1"
#    if 'radio' in r:
#        m_status= smart_str(r['radio'])

    back_myet=""
    if 'hdnBackUrl' in r:
        back_myet = '<span><a href=' + smart_str(r['hdnBackUrl']) + '>Back to Lesson</a><br></span>'

    s=[i.strip() for i in ssplit(smart_str(r['qin'].replace(', ',' : ') ))]

    
    cloze_result=[]
    text_result=[]
    for i in s:
        textin, distractorin = sen_dis(i, item_no)#sen_dis(i, item_no, f_status, m_status)
        for j in distractorin:
            cloze_result.append(j)
        text_result.append(" ".join(textin).replace(" .",".").replace(' : ',', ')) # merge to sentence
    
    request.session['blankText']=" ".join(text_result)
    request.session['blankItem']=cloze_result
    request.session['backMyET']=back_myet
        
    return render_to_response('distractor.html', {'data': cloze_result, "text": " ".join(text_result), 'myet': back_myet}) #merge to paragraph

