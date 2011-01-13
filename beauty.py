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
s = set()

if l > 0:
	for i in range(l):
		soup = getSoup("http://sharg.pl/ajax/items_list.php?c_id=87&page_index="+str(i+1))
		for i in soup.table.findAll('a'):
			s.add(i['href'].replace('item.php?nav=',''))
else:
		for i in soup.table.findAll('a'):
			s.add(i['href'].replace('item.php?nav=',''))

d={}
while len(s): d[s.pop()]={}

for k,v in d.items(): print "%s=%s" % (k,v)

soup = getSoup("http://sharg.pl/")
d2={}
import re
p = re.compile(r'c_id=(?P<word>.+)&')
for i in soup('div',"menu"): m=p.search(i.a['href']); d2[m.group('word')]= i.a.string.strip();

for k,v in d2.items(): print "%s=%s" % (k,v)

logfile = open('categories.txt', 'w')
for k,v in d2.items(): logfile.write(("%s=%s" % (k,v)).encode("utf-8"))
logfile.close()
#TODO
#unique list or just set
#http://www.peterbe.com/plog/uniqifiers-benchmark
#docs.python.org/release/2.5.2/lib/types-set.html
#docs.python.org/tutorial/datastructures.html#sets
#docs.python.org/library/sets.html
#iterate over set mail.python.org/pipermail/python-bugs-list/2005-August/030069.html
