'''
Created on 23 déc. 2013

@author: tolerantjoker
'''
from lxml import html
from lxml.html.clean import clean_html

tree = html.parse('http://www.example.com')
tree = clean_html(tree)
text = tree.getroot().text_content()
print(text)