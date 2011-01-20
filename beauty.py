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


def getSoup(url):
    usock = urllib.urlopen(url)
    htmlSource = usock.read()
    usock.close()
    #commented because i search for &nbsp; in source, so it unescaping must be done later
    #htmlSource = unescape(htmlSource)
    return BeautifulSoup(''.join(htmlSource))

def getfileorurl(url):
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

url = 'http://sharg.pl/ajax/items_list.php?c_id=87'
soup = getfileorurl(url)
#print soup.prettify()
#print vars (soup)
l = len(soup.div('a'))
navs1 = set()

if l > 0:
    for i in range(l):
        url='http://sharg.pl/ajax/items_list.php?c_id=87&page_index='+str(i+1)
        soup = getfileorurl(url)
        for i in soup.table.findAll('a'):
            navs1.add(i['href'].replace('item.php?nav=',''))
else:
    for i in soup.table.findAll('a'):
        navs1.add(i['href'].replace('item.php?nav=',''))

navs2={}
while len(navs1): navs2[navs1.pop()]={}

for k,v in navs2.items(): print "%s=%s" % (k,v)

print "\nnow categories"
url='http://sharg.pl/index.php'
soup = getfileorurl(url)
cats={}
import re
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"):
    m=p.search(i.a['href'])
    cats[m.group('word')]=unescape(i.a.string.strip())

for k,v in cats.items(): print ("%s=%s" % (k,v))

logfile = open('categories.txt', 'w')
for k,v in cats.items(): logfile.write(("%s=%s" % (k,v))+'\n')
logfile.close()
print "\nnow subcategories"
url='http://sharg.pl/items.php?c_id=123'
soup = getfileorurl(url)
subcs={}
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"):
    if "&nbsp;|&nbsp;" in str(i):
        m=p.search(i.a['href'])
        subcs[m.group('word')]=unescape(i.a.string.strip())

logfile = open('subcategories.txt', 'w')
for k,v in subcs.items(): logfile.write(("%s=%s" % (k,v))+'\n')
logfile.close()

for k,v in subcs.items(): print "%s=%s" % (k,v)

#TODO
#unique list or just set
#http://www.peterbe.com/plog/uniqifiers-benchmark
#docs.python.org/release/2.5.2/lib/types-set.html
#docs.python.org/tutorial/datastructures.html#sets
#docs.python.org/library/sets.html
#iterate over set mail.python.org/pipermail/python-bugs-list/2005-August/030069.html
