# -*- coding: utf-8 -*-
import codecs
import re
import pprint 
import sys
import MeCab
import glob
import nltk

##### メソッド定義（開始）#####

## 日本語を扱うメソッド ##
def convertJapanese(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

## IT用語が入ったテキストファイルを読み込む ##
def readText(f):
    word = f.readline()
    word = word.strip('\n') # 改行コードを取り除く
    itWordsList.append(word) # リストに追加
    return word

## IT用語のリストを作成する ##
def makeWordList():
    f = codecs.open('itwords.txt', 'r', 'utf-8') # IT用語が書かれたテキストファイル
    word = readText(f)
    while word: # wordが読み込める限り処理を続ける
        #print word
        word = readText(f)
    f.close
    #print(convertJapanese(itWordsList))

## IT用語が入っているかどうか確認 ##
def checkITWords(file):
    #f = open('sns.txt') # 検索をかけたいテキストファイル
    for line in open(file, 'r'):
        counter = 0
        #line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        mor = MorphologicalAnalysis(line)
        #while line:
        for i in range(0, len(mor)):
            for j in range(0, ITWORDS): 
                #if (itWordsList[j] in line): # IT用語が文章に含まれていないか確認
                if (itWordsList[j] == mor[i]): # IT用語が文章に含まれていないか確認
                    #print itWordsList[j]
                    #print mor[i]
                    counter += 1
            #line = f.readline()
        #file.close
    return counter, len(mor)

## 形態素解析を行うメソッド ##
def MorphologicalAnalysis(line):
    textList = []    # 形態素解析結果のリスト
    line_encode = line.encode('utf-8')
    tagger = MeCab.Tagger ("-Owakati")
    node = tagger.parseToNode(line_encode)
    while node:
        #print node.surface # 形態素解析結果を出力
        sur = node.surface
        sur_decode = sur.decode('utf-8')
        textList.append(sur_decode)
        node = node.next
    #print(convertJapanese(textList)) # 形態素解析結果のリストを出力
    return textList

##### メソッド定義（終了）#####


# 空のリストを生成
itWordsList = [] # IT用語のリスト
ITWORDS = 9185 # 確認するIT用語の数を指定

# IT用語が入ったテキストを開いて読み込む
makeWordList()

# IT用語が入っているかどうか確
for file in glob.glob('e-words_50/*.txt'):
    #print file
    counter, morNum = checkITWords(file)
    #print morNum, counter, float(counter)/morNum
    print file, float(counter)/morNum

