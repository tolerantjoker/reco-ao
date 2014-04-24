# -*- coding: UTF-8 -*-
'''
Created on 23 déc. 2013

@author: tolerantjoker
'''
import treetaggerwrapper
from nltk import wordpunct_tokenize
# Construction et configuration du wrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='C:\Program Files\TreeTagger',
  TAGINENC='utf-8',TAGOUTENC='utf-8')
# Utilisation
tokens = wordpunct_tokenize(u"TRAVAUX DE RENFORCEMENT DES PARKINGS AVIONS 4 - 5 - 6 - 12 .")
tags = tagger.TagText(tokens, encoding="utf-8")
tags_kept = [tag for tag in tags if tag.split('\t')[1] == 'NOM']
for tag in tags:
    print(tag.split('\t'))
print()
for tag in tags_kept:
    print(tag.split('\t'))