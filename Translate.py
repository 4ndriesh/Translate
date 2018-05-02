# coding:utf-8

from nltk.stem import PorterStemmer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def open_file():
    sq = sql_db()
    lemmatizer = WordNetLemmatizer()
    # nltk.download("all")
    example_sent = "that was first spoken in early medieval England and is now the global lingua franca"

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(example_sent)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    ps = PorterStemmer()



    for word_lem in filtered_sentence:
        tmp = lemmatizer.lemmatize(word_lem,pos="n")
        tmp = lemmatizer.lemmatize(tmp, pos="v")
        # tmp = lemmatizer.lemmatize(tmp, pos="a")
        # tmp = lemmatizer.lemmatize(tmp, pos="r")
        # r = ps.stem(tmp)
        print(tmp)
        sq.add_sql_db(tmp,k[0])
    #
    # print(word_lem)
    #

