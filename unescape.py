# -*- coding: utf-8 -*-
#effbot.org/zone/re-sub.htm#unescape-html
import re, htmlentitydefs
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text=m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    #return re.sub("&#?\w+;", fixup, text)
    #when i entered x like below, it was ok
    #>>> x=u'ó&nbsp;&#324;'
    #>>> x
    #u'\xf3&nbsp;&#324;'
    #>>> print unescape.unescape(x)
    #ó ń

#i had to use decode, because in python console when i enter
#>>> x='ó&nbsp;&#324;'
#>>> x
#'\xc3\xb3&nbsp;&#324;'
#>>> print unescape.unescape(x)
#UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: ordinal not in range(128)

#but that worked
#>>> print unescape.unescape((x).decode('utf-8'))

    return re.sub("&#?\w+;", fixup, text.decode('utf-8'))

#print re.sub("&#\d{3}", lambda m: unichr(int(m.group(0)[2:])), text))
#stackoverflow.com/questions/53224/getting-international-characters-from-a-web-page#53246
#w3.org/QA/2008/04/unescape-html-entities-python.html

#>>> print file('text.txtm).read()
#>>> file=open('text.txt')
#>>> for line in file: print line
#>>> reload(unescape)
