# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
from sql_dp import sql_db
import sys
from ya_translate import ya_translate
from open_file import open_file
from lemmatizer import lemmatizer


if __name__ == "__main__":
    print('sdfsdf')
    of=open_file()
    sq = sql_db()

    row=[]
    yt = ya_translate()
    lem=lemmatizer()
    for filtered_sentence in of.read_file():
        if filtered_sentence:
            for words in filtered_sentence:
                if len(words)>2:
                    lemm_word=lem.lemm(words)
                    if not sq.searh_word(lemm_word):
                        print(lemm_word)
                        translate_word=yt.get_english_words(lemm_word)
                        if translate_word:
                            sq.add_sql_db(lemm_word, translate_word)
    sq.sql_to_xls()

    del sq
    del of
    del yt
