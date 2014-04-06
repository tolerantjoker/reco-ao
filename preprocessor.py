# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''

import re
from bs4 import BeautifulSoup
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer

class Preprocessor(object):
    '''
    classdocs
    '''
    def __call__(self, html):
        raw = Preprocessor.clean_html(html)
        raw = Preprocessor.clean_raw(raw)
        tokens = Preprocessor.tokenize(raw)
        tokens = Preprocessor.clean_stop_words(tokens)
        tokens = Preprocessor.normalize(tokens)
        return tokens
        
    @staticmethod
    def clean_html(html):
#         return BeautifulSoup(html).getText()
        return nltk.clean_html(html)
    
    @staticmethod
    def clean_raw(raw):
        '''
        Fonction qui supprime toutes les mots et valeurs non porteurs de sens
        |([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6}) --> e-mail
        |(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/? --> url
        |\d{1,2}\s?[hH]\s?\d{0,2} --> horaire
        |[+-]?(\d+\.\d+|\d+\.|\.\d+) --> valeur flottante
        |[+-]?\d+ --> valeur entière
        |\w' --> les contractions d', l', etc.
        |[!"#$%&\'()*+,./:;<=>?@[\]\\^_`{|}~-] --> les ponctuations 
        '''
#         punct = ''.join([p for p in string.punctuation])
        reg_words = r'''(?x)
        ([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})
        |(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?
        |\d{1,2}\s?[hH]\s?\d{0,2}
        |[+-]?(\d+\.\d+|\d+\.|\.\d+)
        |[+-]?\d+
        |\w'
        |(\w\.)+(\w)?
        |\.\.\.
        |[!"#$%&\'()*+,./:;<=>?@[\]\\^_`{|}~-«»°’-]
        '''
        raw = re.sub(reg_words, r'', raw)
        return raw
#             
    @staticmethod
    def tokenize(raw):
        tokenizer = WordPunctTokenizer()
        return tokenizer.tokenize(raw.decode('utf8'))
    
    @staticmethod
    def clean_stop_words(tokens):
        filtered_word_list = stopwords.words('french') + stopwords.words('english') + stopwords.words('german')
        return [w for w in tokens if w not in filtered_word_list]
    
    @staticmethod
    def normalize(tokens):
        stemmer = SnowballStemmer('french')
        return list(set([stemmer.stem(w.lower()) for w in tokens]))
        # return list(set([w.lower() for w in tokens]))
    
