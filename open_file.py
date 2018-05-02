# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.data.path.append("/home/andrey/nltk_data")

class open_file(object):
    # def __init__(self):

    def tokens(self,example_sent):
        # nltk.download("all")
        intab = "/.–'’-0123456789"
        outtab = "                "
        trantab = str.maketrans(intab, outtab)
        example_sent = example_sent.translate(trantab)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(example_sent)
        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w.lower())
        return filtered_sentence

    def read_file(self):
        with open('eng_file.txt', 'r', encoding='utf-8') as eng_file:
            for sent in eng_file:
                yield(self.tokens(sent))

