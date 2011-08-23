import re
import urllib2


def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)    

def getHTML(query):
    queryText=query.replace(' ','%20')
    urlin='http://nlp.stanford.edu:8080/parser/?query='+queryText
    responseHTML=urllib2.urlopen(urlin).read()
    
    
    taggingEx=re.compile('<h3>Tagging</h3>([^\B]+)<h3>Parse</h3>')
    t=taggingEx.findall(responseHTML)
    
    parseEx=re.compile('<h3>Parse</h3>([^\B]+)<h3>Typed dependencies</h3>')
    p=parseEx.findall(responseHTML)
    
    dependEx=re.compile('<h3>Typed dependencies</h3>([^\B]+)<h3>Typed dependencies, collapsed</h3>')
    d=dependEx.findall(responseHTML)
    
    
    return remove_extra_spaces(remove_html_tags(t[0]))+'\n'+remove_extra_spaces(remove_html_tags(p[0]))+'\n'+remove_extra_spaces(remove_html_tags(d[0]))


#print getHTML("Dont eat too much medicine.")
