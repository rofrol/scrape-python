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

def navsenter(lev1, lev2):
    #print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
    #print 'wchodze do navsenter'
    global cats
    global navs
    global liczbaproduktowlev2allstep
    global liczbaproduktowlev2all
    #print cats[lev1]['name']+':'+cats[lev1]['lev2'][lev2]['name']
    elemnastrone=45
    baseurl = 'http://sharg.pl/ajax/items_list.php?c_id='+str(lev2)+'&items_count='+str(elemnastrone)
    soup = getfileofurl(baseurl)
    s = re.compile(r'Liczba produktów: (?P<word>.+)')
    n = s.search(str(soup))
    liczbaproduktowlev2=int(n.group('word'))
    #print 'liczbaproduktowlev2='+str(liczbaproduktowlev2)
    liczbaproduktowlev2all+=liczbaproduktowlev2
    liczbastron=int(ceil(liczbaproduktowlev2/float(elemnastrone)))
    #print 'liczbastron='+str(liczbastron)
    liczbaproduktowlev2step=0
    for i in range(liczbastron):
        url=baseurl+'&page_index='+str(i+1)
        print url
        soup = getfileofurl(url)
        t = re.compile(r'\[(?P<word>T.+)\]')
        o = t.findall(str(soup))
        for nav in o:
            if nav == 'T001885':
                logfile = open('fucked.html', 'w')
                logfile.write(unescape(str(soup)))
                logfile.close()
                print nav
                sys.exit(1)
            if nav in navs:
                #print 'dupl ^^^ here'
                if lev1 in navs[nav]['cats']:
                    navs[nav]['cats'][lev1].add(lev2)
                else:
                    navs[nav]['cats'][lev1]=set()
                    navs[nav]['cats'][lev1].add(lev2)
            else:
                navs[nav]={}
                navs[nav]['cats']={}
                navs[nav]['cats'][lev1]=set()
                navs[nav]['cats'][lev1].add(lev2)
            liczbaproduktowlev2step+=1
    liczbaproduktowlev2allstep+=liczbaproduktowlev2step
    """
    print 'liczbaproduktowlev2='+str(liczbaproduktowlev2)
    print 'liczbaproduktowlev2step='+str(liczbaproduktowlev2step)
    print 'liczbaproduktowlev2all='+str(liczbaproduktowlev2all)
    print 'liczbaproduktowlev2allstep='+str(liczbaproduktowlev2allstep)
    #"""
    if not liczbaproduktowlev2step == liczbaproduktowlev2:
        print 'bad!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '+str(liczbaproduktowlev2step)+'!='+str(liczbaproduktowlev2)
        sys.exit(1)

fname='dupl.txt'
import os
if os.path.isfile(fname): os.remove(fname)

navs={}
liczbaproduktowlev2allstep=0

print "\nnow categories"
url='http://sharg.pl/index.php'
soup = getfileofurl(url)
cats={}
liczbaproduktowlev1all=0
liczbaproduktowlev2all=0
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
    liczbaproduktowlev1=int(n.group('word'))
    #print "cccccccccccccccccccccccc"
    #print 'liczbaproduktowlev1='+str(liczbaproduktowlev1)
    liczbaproduktowlev1all+=liczbaproduktowlev1
    p = re.compile(r'c_id=(?P<word>.+)&')
    for i in soup('div',"menu"):
        if "&nbsp;|&nbsp;" in str(i):
            m=p.search(i.a['href'])
            key=m.group('word')
            value=unescape(i.a.string.strip())
            cats[k]['lev2'][key]={'name':value}
            navsenter(k, key)

print "wypisuje cats"
for k,v in cats.items():
    print str(k)+"="+v['name']
    for l,m in v['lev2'].items():
        print '\t'+str(l)+'='+m['name']

print "wypisuje navs"
for k,v in navs.items():
    print k
    for i,j in v['cats'].items():
        print '\t'+cats[i]['name']
        for x in j:
            print '\t\t'+cats[i]['lev2'][x]['name']

print 'liczbaproduktowlev1all='+str(liczbaproduktowlev1all)
print 'liczbaproduktowlev2all='+str(liczbaproduktowlev2all)
print 'liczbaproduktowlev2allstep='+str(liczbaproduktowlev2allstep)
print 'len(navs)='+str(len(navs))

navsall={}
elemnastrone=45
baseurl = 'http://sharg.pl/ajax/items_list.php?items_count='+str(elemnastrone)
soup = getfileofurl(baseurl)
s = re.compile(r'Liczba produktów: (?P<word>.+)')
n = s.search(str(soup))
liczbaproduktowall=int(n.group('word'))
print 'liczbaproduktowall='+str(liczbaproduktowall)
liczbastron=int(ceil(liczbaproduktowall/float(elemnastrone)))
print 'liczbastron='+str(liczbastron)
liczbaproduktowallstep=0
for i in range(liczbastron):
    url=baseurl+'&page_index='+str(i+1)
    print url
    soup = getfileofurl(url)
    t = re.compile(r'\[(?P<word>T.+)\]')
    o = t.findall(str(soup))
    for nav in o:
        navsall[nav]={}
        liczbaproduktowallstep+=1

print 'liczbaproduktowall='+str(liczbaproduktowlev2all)
print 'liczbaproduktowallstep='+str(liczbaproduktowlev2allstep)
print 'len(navsall)='+str(len(navsall))

for key in navsall.keys():
    if not key in navs:
            print key

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
#all products 1597 http://sharg.pl/ajax/items_list.php?m_id=0&search=&x=63&y=5
#unique list or just set
#http://www.peterbe.com/plog/uniqifiers-benchmark
#docs.python.org/release/2.5.2/lib/types-set.html
#docs.python.org/tutorial/datastructures.html#sets
#docs.python.org/library/sets.html
#iterate over set mail.python.org/pipermail/python-bugs-list/2005-August/030069.html
