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

    htmlSource = unescape(htmlSource)
    return BeautifulSoup(''.join(htmlSource))

soup = getSoup("http://sharg.pl/ajax/items_list.php?c_id=87")
#print soup.prettify()
#print vars (soup)
l = len(soup.div('a'))
navs1 = set()

if l > 0:
    for i in range(l):
        soup = getSoup("http://sharg.pl/ajax/items_list.php?c_id=87&page_index="+str(i+1))
        for i in soup.table.findAll('a'):
            navs1.add(i['href'].replace('item.php?nav=',''))
else:
    for i in soup.table.findAll('a'):
        navs1.add(i['href'].replace('item.php?nav=',''))

navs2={}
while len(navs1): navs2[navs1.pop()]={}

for k,v in navs2.items(): print "%s=%s" % (k,v)

soup = getSoup("http://sharg.pl/")
cats={}
import re
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"): m=p.search(i.a['href']); cats[m.group('word')]=i.a.string.strip();

for k,v in cats.items(): print "%s=%s" % (k,v)

logfile = open('categories.txt', 'w')
for k,v in cats.items(): logfile.write(("%s=%s" % (k,v)).encode("utf-8")+'\n')
logfile.close()

print "now subcategory"
soup = BeautifulSoup(''.join(file('items.php?c_id=149').read()))
subcs={}
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"):
    if "&nbsp;|&nbsp;" in str(i):
        m=p.search(i.a['href'])
        subcs[m.group('word')]=i.a.string.strip();

for k,v in subcs.items(): print "%s=%s" % (k,v)

#TODO
#unique list or just set
#http://www.peterbe.com/plog/uniqifiers-benchmark
#docs.python.org/release/2.5.2/lib/types-set.html
#docs.python.org/tutorial/datastructures.html#sets
#docs.python.org/library/sets.html
#iterate over set mail.python.org/pipermail/python-bugs-list/2005-August/030069.html
