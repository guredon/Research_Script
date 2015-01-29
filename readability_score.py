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

def calc_readability(filename, char, phrase, predicate, hiragana, idf_sum, idf_ave, itwords):

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
    text_idf_sum  = float(idf_sum)
    text_idf_ave  = float(idf_ave)
    rate_itwords  = float(itwords)
    res           = 0
    
    # 2008
    #res = -0.183 * ave_char + 0.823 * ave_phrase - 0.288 * ave_predicate - 0.189 * rate_hiragana + 20.027 + text_idf_ave
    
    # 2010-01
    #res = -0.145 * rate_hiragana + 0.587 * ave_predicate + 14.016 + text_idf_ave

    # 2010-09-(1)
    res = -147.9 + (3.601E-04) * pow(rate_hiragana, 3) - (8.772E-02) * pow(rate_hiragana, 2) + 6.651 * rate_hiragana + 3.679 * ave_phrase + (3.142E-04) * pow(rate_hiragana, 2) * ave_char - (3.986E-04) * pow(rate_hiragana, 2) * ave_phrase - (3.207E-04) * rate_hiragana * pow(ave_char, 2) - (3.109E-02) * rate_hiragana * ave_char - (7.968E-03) * rate_hiragana * pow(ave_phrase, 2) + (3.486E-03) * rate_hiragana * ave_char * ave_phrase
    
    # 2010-09-(2)
    res = -129.1 + 5.96 * rate_hiragana - (8.106E-02) * pow(rate_hiragana, 2) + (3.496E-04) * pow(rate_hiragana, 3) - (1.548E-01) * ave_char + (4.864E-02) * pow(ave_phrase, 2)

    # 2010-09-(3)
    res = 31.79 - (3.043E-01) * rate_hiragana - 2.322 * ave_char + 9.1 * ave_phrase - 1.647 * ave_predicate + (2.170E-02) * rate_hiragana * ave_char - (8.371E-02) * rate_hiragana * ave_phrase + (1.6866E-01) * ave_char * ave_predicate - (5.661E-01) * ave_phrase * ave_predicate


    print filename, res


f = open(sys.argv[1], 'rt')
try:
    reader = csv.reader(f)
    fieldnames = next(reader) # 最初の1行を取り出す
    for row in reader:
        calc_readability(row[0].decode('utf-8'), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
finally:
    f.close()

