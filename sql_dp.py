# coding:utf-8
__author__ = 'BiziurAA'
import sqlite3
from XlsxWriter import cl_xlsxwriter

class sql_db(object):
    def __init__(self):
        self._con = sqlite3.connect('Endlish_words.db')
        self._cur = self._con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS Endlish_words (id INTEGER PRIMARY KEY AUTOINCREMENT,Words TEXT, Translates TEXT);
                    CREATE TRIGGER  IF NOT EXISTS Endlish_words BEFORE INSERT ON Endlish_words BEGIN SELECT CASE WHEN EXISTS(SELECT Words FROM Endlish_words WHERE new.Words=Words) THEN RAISE(ABORT,"Дубликат")END;END;;"""
        try:
            self._cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print("Erroe:", err)
        else:
            print("Endlish_words is open")
    def __del__(self):
        self._cur.close()
        self._con.close()

    def add_sql_db(self,Eng_Words,Translates):
        try:
            sql = "INSERT INTO Endlish_words (Words,Translates) VALUES('{0}','{1}');".format(Eng_Words,Translates)
            self._cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print(u"Ошибка: {0}-".format(Eng_Words), err)
        else:
            print("-->>> {0}-{1}".format(Eng_Words,Translates))

    def searh_word(self, Eng_Words):
        try:
            sql = "SELECT Words FROM Endlish_words WHERE Words='{0}';".format(Eng_Words)
            self._cur.execute(sql)
        except sqlite3.DatabaseError as err:
            print(u"Ошибка: {0}-".format(Eng_Words), err)
        else:
            return self._cur.fetchone()

    def sql_to_xls(self):
        xl = cl_xlsxwriter()
        try:
            sql = "SELECT Words,Translates FROM Endlish_words"
            self._cur.execute(sql)
            for row in self._cur:
                xl.def_xlsxwriter(row[0], row[1])

        except sqlite3.DatabaseError as err:
            print(u"Ошибка:", err)
        else:
            print(u"Add_xls_file")
