# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
from nltk.stem import WordNetLemmatizer

class lemmatizer(object):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
    def lemm(self,word_lem):
        tmp = self.lemmatizer.lemmatize(word_lem, pos="n")
        tmp = self.lemmatizer.lemmatize(tmp, pos="v")

        tmp = self.lemmatizer.lemmatize(tmp, pos="a")
        tmp = self.lemmatizer.lemmatize(tmp, pos="r")
        return tmp
        # r = ps.stem(tmp)