# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''

from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

class Preprocessor(object):
    '''
    classdocs
    '''
    def __call__(self, html):
        raw = Preprocessor.clean_html(html)
        tokens = Preprocessor.tokenize(raw)
        tokens = Preprocessor.clean_stop_words(tokens)
        tokens = Preprocessor.normalize(tokens)
        return tokens
        
    @staticmethod
    def clean_html(html):
        #return BeautifulSoup(html).getText()
        return nltk.clean_html(html)
        
    @staticmethod
    def tokenize(raw):
        tokenizer = RegexpTokenizer(r'''(?x)
        \d+(\.\d+)?\s*%
        |([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})
        |(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?
        |\w'
        |\w+
        |[^\w\s]
        ''')
        return tokenizer.tokenize(raw)
    
    @staticmethod
    def clean_stop_words(tokens):
        filtered_word_list = stopwords.words('french')
        return [w for w in tokens if w not in filtered_word_list]
    
    @staticmethod
    def normalize(tokens):
        stemmer = SnowballStemmer('french')
        return list(set([stemmer.stem(w.lower()) for w in tokens]))
    