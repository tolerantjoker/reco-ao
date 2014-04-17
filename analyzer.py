# -*- coding: UTF-8 -*-
'''
Created on 20 mars 2014

@author: tolerantjoker
'''

import re
import enchant
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import FrenchStemmer
from nltk import word_tokenize, wordpunct_tokenize
from nltk.tokenize.regexp import RegexpTokenizer

class Analyzer(object):
    '''
    classdocs
    '''
    def __call__(self, html):
        raw = Analyzer.clean_html(html)
#         raw = Analyzer.clean_raw(raw)
        tokens = Analyzer.tokenize(raw)
        tokens = Analyzer.clean_stop_words(tokens)
        tokens = Analyzer.normalize(tokens)
        return tokens
    
    @staticmethod
    def clean_html(html):
#         return BeautifulSoup(html).getText()
        return nltk.clean_html(html).decode('utf-8')
    
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

        reg_words = r'''(?xi)
        ((IX)|(IV)|(VI{0,3})|[^V](I{1,3})[^V])\.
        |([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})
        |(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?
        |\$?\d+(\.\d+)?%?
        |\d{1,2}\s?[hH]\s?\d{0,2}
        |[+-]?(\d+\.\d+|\d+\.|\.\d+)
        |[+-]?\d+
        |[a-z]+[\'\’\´\`\ʻ\′]
        |([a-z]\.)+
        |\.\.\.
        |[!"#$€%&\'()*+,./:;<=>?@[\]\\^_`{|}~-«»°’-]
        '''
        raw = re.sub(reg_words, r' ', raw.decode('utf8'))
        return raw
#             
    @staticmethod
    def tokenize(raw):
#         tokens = wordpunct_tokenize(raw.decode('utf8'))
#         return nltk.Text(tokens,'utf8')
        tokenizer = RegexpTokenizer('''(?xi)
        ((IX)|(IV)|(VI{0,3})|[^V](I{1,3})[^V])\.
        |([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})
        |(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?
        |\d+(\.\d+)?\s*%
        |\d{1,2}\s?[hH]\s?\d{0,2}
        |[+-]?(\d+\.\d+|\d+\.|\.\d+)
        |[+-]?\d+
        |\w+
        |\.\.\.
        |[^\w\s]
        ''')
        tokens = tokenizer.tokenize(raw)
        return tokens
    
    @staticmethod
    def clean_stop_words(text):
#         d = enchant.Dict('fr_FR')
#         tokens = [w.lower() for w in text if d.check(w)]
        tokens = [w.lower() for w in text]
        raw_stopword_list = ["Ap.", "Apr.", "GHz", "MHz", "USD", "a", "afin", "ah", "ai", "aie", "aient", "aies", "ait", "alors", "après", "as", "attendu", "au", "au-delà", "au-devant", "aucun", "aucune", "audit", "auprès", "auquel", "aura", "aurai", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions", "aurons", "auront", "aussi", "autour", "autre", "autres", "autrui", "aux", "auxdites", "auxdits", "auxquelles", "auxquels", "avaient", "avais", "avait", "avant", "avec", "avez", "aviez", "avions", "avons", "ayant", "ayez", "ayons", "b", "bah", "banco", "ben", "bien", "bé", "c", "c'", "c'est", "c'était", "car", "ce", "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là", "celà", "cent", "cents", "cependant", "certain", "certaine", "certaines", "certains", "ces", "cet", "cette", "ceux", "ceux-ci", "ceux-là", "cf.", "cg", "cgr", "chacun", "chacune", "chaque", "chez", "ci", "cinq", "cinquante", "cinquante-cinq", "cinquante-deux", "cinquante-et-un", "cinquante-huit", "cinquante-neuf", "cinquante-quatre", "cinquante-sept", "cinquante-six", "cinquante-trois", "cl", "cm", "cm²", "comme", "contre", "d", "d'", "d'après", "d'un", "d'une", "dans", "de", "depuis", "derrière", "des", "desdites", "desdits", "desquelles", "desquels", "deux", "devant", "devers", "dg", "différentes", "différents", "divers", "diverses", "dix", "dix-huit", "dix-neuf", "dix-sept", "dl", "dm", "donc", "dont", "douze", "du", "dudit", "duquel", "durant", "dès", "déjà", "e", "eh", "elle", "elles", "en", "en-dehors", "encore", "enfin", "entre", "envers", "es", "est", "et", "eu", "eue", "eues", "euh", "eurent", "eus", "eusse", "eussent", "eusses", "eussiez", "eussions", "eut", "eux", "eûmes", "eût", "eûtes", "f", "fait", "fi", "flac", "fors", "furent", "fus", "fusse", "fussent", "fusses", "fussiez", "fussions", "fut", "fûmes", "fût", "fûtes", "g", "gr", "h", "ha", "han", "hein", "hem", "heu", "hg", "hl", "hm", "hm³", "holà", "hop", "hormis", "hors", "huit", "hum", "hé", "i", "ici", "il", "ils", "j", "j'", "j'ai", "j'avais", "j'étais", "jamais", "je", "jusqu'", "jusqu'au", "jusqu'aux", "jusqu'à", "jusque", "k", "kg", "km", "km²", "l", "l'", "l'autre", "l'on", "l'un", "l'une", "la", "laquelle", "le", "lequel", "les", "lesquelles", "lesquels", "leur", "leurs", "lez", "lors", "lorsqu'", "lorsque", "lui", "lès", "m", "m'", "ma", "maint", "mainte", "maintes", "maints", "mais", "malgré", "me", "mes", "mg", "mgr", "mil", "mille", "milliards", "millions", "ml", "mm", "mm²", "moi", "moins", "mon", "moyennant", "mt", "m²", "m³", "même", "mêmes", "n", "n'avait", "n'y", "ne", "neuf", "ni", "non", "nonante", "nonobstant", "nos", "notre", "nous", "nul", "nulle", "nº", "néanmoins", "o", "octante", "oh", "on", "ont", "onze", "or", "ou", "outre", "où", "p", "par", "par-delà", "parbleu", "parce", "parmi", "pas", "passé", "pendant", "personne", "peu", "plus", "plus_d'un", "plus_d'une", "plusieurs", "pour", "pourquoi", "pourtant", "pourvu", "près", "puisqu'", "puisque", "q", "qu", "qu'", "qu'elle", "qu'elles", "qu'il", "qu'ils", "qu'on", "quand", "quant", "quarante", "quarante-cinq", "quarante-deux", "quarante-et-un", "quarante-huit", "quarante-neuf", "quarante-quatre", "quarante-sept", "quarante-six", "quarante-trois", "quatorze", "quatre", "quatre-vingt", "quatre-vingt-cinq", "quatre-vingt-deux", "quatre-vingt-dix", "quatre-vingt-dix-huit", "quatre-vingt-dix-neuf", "quatre-vingt-dix-sept", "quatre-vingt-douze", "quatre-vingt-huit", "quatre-vingt-neuf", "quatre-vingt-onze", "quatre-vingt-quatorze", "quatre-vingt-quatre", "quatre-vingt-quinze", "quatre-vingt-seize", "quatre-vingt-sept", "quatre-vingt-six", "quatre-vingt-treize", "quatre-vingt-trois", "quatre-vingt-un", "quatre-vingt-une", "quatre-vingts", "que", "quel", "quelle", "quelles", "quelqu'", "quelqu'un", "quelqu'une", "quelque", "quelques", "quelques-unes", "quelques-uns", "quels", "qui", "quiconque", "quinze", "quoi", "quoiqu'", "quoique", "r", "revoici", "revoilà", "rien", "s", "s'", "sa", "sans", "sauf", "se", "seize", "selon", "sept", "septante", "sera", "serai", "seraient", "serais", "serait", "seras", "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sinon", "six", "soi", "soient", "sois", "soit", "soixante", "soixante-cinq", "soixante-deux", "soixante-dix", "soixante-dix-huit", "soixante-dix-neuf", "soixante-dix-sept", "soixante-douze", "soixante-et-onze", "soixante-et-un", "soixante-et-une", "soixante-huit", "soixante-neuf", "soixante-quatorze", "soixante-quatre", "soixante-quinze", "soixante-seize", "soixante-sept", "soixante-six", "soixante-treize", "soixante-trois", "sommes", "son", "sont", "sous", "soyez", "soyons", "suis", "suite", "sur", "sus", "t", "t'", "ta", "tacatac", "tandis", "te", "tel", "telle", "telles", "tels", "tes", "toi", "ton", "toujours", "tous", "tout", "toute", "toutefois", "toutes", "treize", "trente", "trente-cinq", "trente-deux", "trente-et-un", "trente-huit", "trente-neuf", "trente-quatre", "trente-sept", "trente-six", "trente-trois", "trois", "très", "tu", "u", "un", "une", "unes", "uns", "v", "vers", "via", "vingt", "vingt-cinq", "vingt-deux", "vingt-huit", "vingt-neuf", "vingt-quatre", "vingt-sept", "vingt-six", "vingt-trois", "vis-à-vis", "voici", "voilà", "vos", "votre", "vous", "w", "x", "y", "z", "zéro", "à", "ç'", "ça", "ès", "étaient", "étais", "était", "étant", "étiez", "étions", "été", "étée", "étées", "étés", "êtes", "être", "ô"]
        filtered_word_list = list(set(raw_stopword_list
                                      + stopwords.words('french') 
                                      ))
#         filtered_word_list = set(stopwords.words('french'))
        return [w for w in tokens if w not in filtered_word_list and w.isalpha()]
    
    @staticmethod
    def normalize(tokens):
        stemmer = FrenchStemmer()
        return list(set([stemmer.stem(w) for w in tokens]))
    
