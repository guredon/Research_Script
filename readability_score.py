# -*- coding: utf-8 -*-

import csv
import sys
import codecs
import re
import pprint 

##### メソッド定義（開始）#####

## 日本語を扱うメソッド ##
def convertJapanese(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

def calc_readability(filename, char, phrase, predicate, hiragana, idf, itwords):

    #print filename
    #print char
    #print phrase
    #print predicate
    #print hiragana
    #print idf

    ave_char      = float(char)
    ave_phrase    = float(phrase)
    ave_predicate = float(predicate)
    rate_hiragana = float(hiragana)
    text_idf      = float(idf)
    rate_itwords  = float(itwords)
    res           = 0
    
    #res = -0.183 * ave_char + 0.823 * ave_phrase - 0.288 * ave_predicate - 0.189 * rate_hiragana + 20.027 + text_idf * 0.01
    
    res = -0.145 * rate_hiragana + 0.587 * ave_predicate + 14.016 + text_idf * 0.01 + rate_itwords

    print res


f = open(sys.argv[1], 'rt')
try:
    reader = csv.reader(f)
    fieldnames = next(reader) # 最初の1行を取り出す
    for row in reader:
        calc_readability(row[0].decode('utf-8'), row[1], row[2], row[3], row[4], row[5], row[6])
finally:
    f.close()

