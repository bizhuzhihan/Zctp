# -*- coding: utf-8 -*-

'''
Usage:
    cat(df, col, threshold, num = 5)
    dog(df, col, word)

# cat function
Function:
    calculate the frequency of words
Input:
    df: a pandas.DataFrame
    col: the label of the selected column (eg. '诊断')
    threshold: the threshold of the freq
    num: the max number of words to be combined, default: 5
Output:
    pd.DataFrame
        freq: the frequency of a word
        words: ...

# dog function
Function:
    match the array of string with a word(string)
Input:
    df: a pandas.DataFrame
    col: the label of the selected column (eg. '诊断')
    word: a string you want to match with
Output:
    array of bool

2019.04.27 written by Zhu.      Verson: 1.1
'''

import pandas as pd
import jieba as jb

# Warehouse
class Warehouse(object):
    def __init__(self, threshold):
        self._words = []
        self._threshold = threshold

    # capturing the words in list into the warehouse
    def capturing(self, diag, num):
        for i in range(len(diag)):
            record = diag[i]
            l = len(record)
            if((l-num+1) > 0):
                j = 0
                while(j < (l-num+1)):
                    if(recognizing(record, j, num)):
                        j = j + recognizing(record, j, num)
                    else:
                        temp = ''
                        for k in range(j, j+num):
                            temp += record[k]
                        self._words.append(temp)
                        j += 1
        return self.summing()

    # calculating the freq of a word
    def summing(self):
        df = pd.DataFrame()
        df['words'] = self._words
        df['freq'] = 1
        df = (df.groupby('words')).sum()
        df = df.sort_values('freq', ascending = False)
        df = df[df['freq'] >= self._threshold]
        df['words'] = df.index
        df.index = range(len(df))
        return df

    # merge warehouse(num) with warehouse(num - 1)
    def merging(self, diag, num, df):
        df2 = self.capturing(diag, num)
        for i in range(len(df2)):
            if(searching(df, df2.loc[i].words)):
                df2 = df2.drop(i)
        df2 = pd.concat([df, df2])
        df2 = df2.sort_values('freq', ascending = False)
        df2.index = range(len(df2))
        return df2

####################################################################################################
# use jieba to split the records into single words
def splitting(diag):
    diag_new = []
    for i in range(len(diag)):
        diag_new.append(jb.lcut(diag[i], cut_all=False))
    return diag_new

####################################################################################################
# recognizing symbols and numbers
def recognizing_1(word):
    s = ord(word[0])
    # upper case
    b1 = ((s >= 65) & (s <= 90))
    # lower case
    b2 = ((s >= 97) & (s <= 122))
    # Chinese
    b3 = ((s >= 19968) & (s <= 40943))
    if(b1|b2|b3):
        return 0
    else:
        return 1

def recognizing(record, pos, num):
    for i in range(0, num):
        if(recognizing_1(record[pos+i])):
            return i+1
    return 0

####################################################################################################
# searching in the list
def matching(record, word, j):
    n = 0
    for k in range(len(word)):
        if(record[j+k] == word[k]):
            n += 1
    return n

def searching(w, word):
    t = 0
    num = len(word)
    for i in range(len(w['words'])):
        r = w['words'][i]
        l = len(r)
        for j in range(l-num+1):
            n = matching(r, word, j)
            if(n >= num):
                t += 1
    return t

####################################################################################################
# main function cat
def cat(df, col, threshold, num = 5):
    diag = splitting(df[col])
    warehouse = Warehouse(threshold)
    warehouse = warehouse.capturing(diag, num)
    while(num > 1):
        num -= 1
        w_t = Warehouse(threshold)
        warehouse = w_t.merging(diag, num, warehouse)
        
    for i in range(len(warehouse)):
        if(len(warehouse['words'][i]) == 1):
            warehouse = warehouse.drop(i)
            
    return warehouse

####################################################################################################
# building a array of matching
##################################################
# searching in one record
def dog_1(record, word):
    n = 0
    for i in range(0, len(record) - len(word) + 1):
        n += (matching(record, word, i, len(word)) == len(word))
    return n

def dog(df, col, word):
    diag = df[col]
    match = []
    for i in range(0, len(diag)):
        if(dog_1(diag[i], word)):
            match.append(1)
        else:
            match.append(0)
    return match