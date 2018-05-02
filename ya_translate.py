# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
from yandex_translate import YandexTranslate

class ya_translate(object):

    def __init__(self):
        self.translate = YandexTranslate('trnsl.1.1.20170417T120755Z.ace07b3e54a7011b.23ef0f7b86f04dff506c4b86bdb4eb547901af1b')

    def get_english_words(self,eng_word):
        tmp_translate_word=self.translate.translate(eng_word,"ru")
        translate_word=tmp_translate_word['text'][0]
        if self.translate.detect(translate_word) in 'ru':
            return translate_word
        else:
            return