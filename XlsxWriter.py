# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'
import xlsxwriter

class cl_xlsxwriter():
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Expenses02.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.row = 0
        self.col = 0
    def def_xlsxwriter(self,lemm_word, translate_word):
        self.worksheet.write(self.row, self.col, lemm_word)
        self.worksheet.write(self.row, self.col + 1, translate_word)
        self.row += 1
