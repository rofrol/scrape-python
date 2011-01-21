#!/usr/bin/python
# -*- coding: UTF-8 -*-

#http://blog.i18n.ro/2010/01/06/using-unicode-console-output-with-python/
#http://blog.notdot.net/2010/07/Getting-unicode-right-in-Python
import codecs, sys
reload(sys)
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

#http://diveintopython.org/html_processing/extracting_data.html
#http://www.crummy.com/software/BeautifulSoup/documentation.html
import urllib
from BeautifulSoup import BeautifulSoup
import re, htmlentitydefs
from unescape import *
from math import ceil
import sys


def getSoup(url):
    usock = urllib.urlopen(url)
    htmlSource = usock.read()
    usock.close()
    #commented because i search for &nbsp; in source, so it unescaping must be done later
    #htmlSource = unescape(htmlSource)
    return BeautifulSoup(''.join(htmlSource))

def getfileofurl(url):
    import os.path
    from urlparse import urlparse
    fname=os.path.basename(urlparse(url).path)+'?'+urlparse(url).query
    if not os.path.isfile('temp/'+fname):
        usock = urllib.urlopen(url)
        htmlSource = usock.read().decode('utf-8')
        logfile = open('temp/'+fname, 'w')
        logfile.write(htmlSource)
        logfile.close()
    return BeautifulSoup(''.join(file('temp/'+fname).read()))

"""
url = 'http://sharg.pl/ajax/items_list.php?c_id=87'
soup = getfileofurl(url)
#print soup.prettify()
#print vars (soup)
l = len(soup.div('a'))
navs1 = set()

if l > 0:
    for i in range(l):
        url='http://sharg.pl/ajax/items_list.php?c_id=87&page_index='+str(i+1)
        soup = getfileofurl(url)
        for i in soup.table.findAll('a'):
            navs1.add(i['href'].replace('item.php?nav=',''))
else:
    for i in soup.table.findAll('a'):
        navs1.add(i['href'].replace('item.php?nav=',''))

navs2={}
while len(navs1): navs2[navs1.pop()]={}

for k,v in navs2.items(): print "%s=%s" % (k,v)
#"""

navs={}
liczbaproduktowallstep=0

def navsenter(lev1, lev2):
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    print 'wchodze do navsenter'
    global cats
    global navs
    global liczbaproduktowallstep
    print cats[lev1]['name']+':'+cats[lev1]['lev2'][lev2]
    elemnastrone=45
    baseurl = 'http://sharg.pl/ajax/items_list.php?c_id='+str(lev2)+'&items_count='+str(elemnastrone)
    soup = getfileofurl(baseurl)
    #l = len(soup.div('a'))
    #print 'liczba stron='+str(l)
    s = re.compile(r'Liczba produktów: (?P<word>.+)')
    n = s.search(str(soup))
    liczbaproduktow=int(n.group('word'))
    print 'liczbaproduktow='+str(liczbaproduktow)
    liczbastron=int(ceil(liczbaproduktow/float(elemnastrone)))
    print 'liczbastron='+str(liczbastron)
    liczba=0
    if liczbastron > 0:
        for i in range(liczbastron):
            url=baseurl+'&page_index='+str(i+1)
            print url
            soup = getfileofurl(url)
            t = re.compile(r'\[(?P<word>T.+)\]')
            o = t.findall(str(soup))
            #print "len(soup.table.findAll('a'))/2="+str(len(soup.table.findAll('a'))/2)
            #for i in soup.table.findAll('a'):
                #nav=i['href'].replace('item.php?nav=','')
            for nav in o:
                print nav
                if nav in navs:
                    print 'cannot add to '+cats[lev1]['name']+' : '+cats[lev1]['lev2'][lev2]
                    print 'bad!!!!!!!!!!!!! '+nav+' already exists in '
                    l1=navs[nav]['lev1']
                    l2=navs[nav]['lev2']
                    print cats[l1]['name']+' : '+cats[l1]['lev2'][l2]
                    sys.exit(1)
                navs[nav]={'lev1':lev1, 'lev2':lev2}
                liczba+=1
    else:
        url=baseurl
        print url
        soup = getfileofurl(url)
        t = re.compile(r'\[(?P<word>T.+)\]')
        o = t.findall(str(soup))
        #print "len(soup.table.findAll('a'))/2="+str(len(soup.table.findAll('a'))/2)
        #for i in soup.table.findAll('a'):
            #nav=i['href'].replace('item.php?nav=','')
        for nav in o:
            print nav
            if nav in navs:
                print nav
                print lev1
                print lev2
                print 'bad!!!!!!!!!!!!! nav already exists'
                sys.exit(1)
            navs[nav]={'lev1':lev1, 'lev2':lev2}
            liczba+=1
    liczbaproduktowallstep+=liczba
    print 'liczba='+str(liczba)
    print 'liczbaproduktowallstep='+str(liczbaproduktowallstep)
    if liczba == liczbaproduktow:
        print 'ok '+str(liczba)+'='+str(liczbaproduktow)
    else:
        print 'bad!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '+str(liczba/2)+'!='+str(liczbaproduktow)
        sys.exit(1)


print "\nnow categories"
url='http://sharg.pl/index.php'
soup = getfileofurl(url)
cats={}
liczbaproduktowall=0
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"):
    m=p.search(i.a['href'])
    key=m.group('word')
    value=unescape(i.a.string.strip())
    cats[key]={'name':value}
    cats[key]['lev2']={}

for k,v in cats.items():
    url = 'http://sharg.pl/items.php?c_id='+str(k)
    soup = getfileofurl(url)
    s = re.compile(r'Liczba produktów: (?P<word>.+)')
    n = s.search(str(soup))
    liczbaproduktow=int(n.group('word'))
    liczbaproduktowall+=liczbaproduktow
    p = re.compile(r'c_id=(?P<word>.+)&')
    for i in soup('div',"menu"):
        if "&nbsp;|&nbsp;" in str(i):
            m=p.search(i.a['href'])
            key=m.group('word')
            value=unescape(i.a.string.strip())
            cats[k]['lev2'][key]=value
            #print '\n'+value
            navsenter(k, key)
#for k,v in navs.items(): print "%s=%s" % (k,v)

print "wypisuje"
for k,v in cats.items():
    print str(k)+"="+v['name']
    for l,m in v['lev2'].items():
        print '\t'+str(l)+'='+str(m)

print 'liczbaproduktowall='+str(liczbaproduktowall)
print 'liczbaproduktowallstep='+str(liczbaproduktowallstep)
print 'len(navs)='+str(len(navs))
"""
logfile = open('categories.txt', 'w')
for k,v in cats.items(): logfile.write(("%s=%s" % (k,v))+'\n')
logfile.close()

print "\nnow subcategories"
url='http://sharg.pl/items.php?c_id=123'
soup = getfileofurl(url)
lev2={}
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"):
    if "&nbsp;|&nbsp;" in str(i):
        m=p.search(i.a['href'])
        lev2[m.group('word')]=unescape(i.a.string.strip())

logfile = open('subcategories.txt', 'w')
for k,v in lev2.items(): logfile.write(("%s=%s" % (k,v))+'\n')
logfile.close()

for k,v in lev2.items(): print "%s=%s" % (k,v)
#"""
#TODO
#unique list or just set
#http://www.peterbe.com/plog/uniqifiers-benchmark
#docs.python.org/release/2.5.2/lib/types-set.html
#docs.python.org/tutorial/datastructures.html#sets
#docs.python.org/library/sets.html
#iterate over set mail.python.org/pipermail/python-bugs-list/2005-August/030069.html
