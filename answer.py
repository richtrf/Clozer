from django.shortcuts import render_to_response

def index(request):
    m=request.REQUEST
    a=m.getlist('ans')
    u=m.getlist('answer_user')
    a=[int(i.encode('utf8')) for i in a ]
    u=[int(i.encode('utf8')) for i in u ]
    t=request.session['blankText']
    d=request.session['blankItem']
    back_myet=request.session['backMyET']
    
    testno=range(1,len(a)+1)
    corrected=[(i3,i1) for i1,i2,i3 in  zip(a,u,testno) if i1<>i2]
    grade=str((len(testno)-len(corrected))*100/len(testno))
    

    
    for i1,i2 in corrected:
        d[i1-1][2]="<font color='red'>%d</font>" % i2
        d[i1-1][1]=d[i1-1][1].replace(d[i1-1][3][i2-1], "<font color='red'>%s</font>" % d[i1-1][3][i2-1])  # d[i1-1][3][i2-1] -> the wrong answer
        
    return render_to_response('answer.html', {\
                                              'text':t , \
                                              'data': d, \
                                              'ans': a, \
                                              'user': u,\
                                              'grade': grade,\
                                              'myet': back_myet
                                              })