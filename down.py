from bs4 import BeautifulSoup
import urllib2
import re
import time
#code:utf-8
fl=['e4','Incubator','JDT','PDE','Platform']
for m in fl:

    url = "https://bugs.eclipse.org/bugs/buglist.cgi?bug_status=VERIFIED&classification=Eclipse&product="+m+"&query_format=advanced&resolution=FIXED"
    baseURL = "https://bugs.eclipse.org/bugs/"
    timeout = 50

    try:
	bugListHTML = urllib2.urlopen(url, timeout = timeout).read()
    except Exception, e:
	print "base URL timeout"
	exit(0)

    soupbase = BeautifulSoup(bugListHTML, "lxml")
    bugtd = soupbase.find_all("td",{"class": "first-child bz_id_column"})
    f=open(m,'w')
    for td in bugtd:
        term={}
	bugid =  td.a['href']
	contentURL = baseURL + bugid
#	print contentURL
	try:
		bugcontent = urllib2.urlopen(contentURL, timeout = timeout).read()
	except Exception, e:
		print "content URL timeout"
		continue

        term['Bugid']=bugid.split('id=')[-1]
	soup = BeautifulSoup(bugcontent, "lxml")
	baseinfo = soup.find("td",id="bz_show_bug_column_1")
        tit=soup.find('span',id="short_desc_nonedit_display")
        term['Title']=tit.get_text()
        tl=baseinfo.table.find_all('tr')
        
        for t in tl:
            ss=re.sub(r'[ ]{2,}','',t.get_text().encode('GBK','ignore')).replace('\n','').split(':')
            if len(ss)>=2:
                term[ss[0]]=ss[1]
        commlist= soup.find_all('pre')
        term['Description']=commlist[0].get_text()
        term['Comments']=[]
        for t in commlist[1:]:
            term['Comments'].append(t.get_text())
        print >>f,term
       # exit(0)
        time.sleep(1)
    f.close()
