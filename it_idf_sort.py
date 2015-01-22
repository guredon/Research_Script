# -*- coding: utf-8 -*-
import codecs
import re
import pprint 
import sys
import MeCab
import glob
import nltk
import math

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
        morListGroup.append(mor)
        #while line:
        for i in range(0, len(mor)):
            for j in range(0, ITWORDS): 
                #if (itWordsList[j] in line): # IT用語が文章に含まれていないか確認
                if (itWordsList[j] in mor[i]): # IT用語が文章に含まれていないか確認
                    #print itWordsList[j]
                    #print mor[i]
                    counter += 1
                    idfITwordsList.append(itWordsList[j])
                    #print (convertJapanese(idfITwordsList))
            #line = f.readline()
        #file.close
    return counter, len(mor)

## 形態素解析を行うメソッド ##
def MorphologicalAnalysis(line):
    morList = []    # 形態素解析結果のリスト
    line_encode = line.encode('utf-8')
    tagger = MeCab.Tagger ("-Owakati")
    node = tagger.parseToNode(line_encode)
    while node:
        #print node.surface # 形態素解析結果を出力
        sur = node.surface
        sur_decode = sur.decode('utf-8')
        morList.append(sur_decode)
        node = node.next
    #print(convertJapanese(morList)) # 形態素解析結果のリストを出力
    return morList

## IDFを求めるメソッド ##
def nltk_idf(morListGroup, idfITwordsList):
        tokens = []
        for morList in morListGroup:
            tokens += morList
        A = nltk.TextCollection(morList)
        #print(convertJapanese(tokens))
        token_types = set(idfITwordsList)
        for token_type in token_types:
            print token_type
            print 'TF = %f' % A.tf(token_type, idfITwordsList)
            print 'IDF = %f' % A.idf(token_type)


## IT用語のIDFを求めるメソッド ##
def calc_idf(morListGroup):
    allCount = {}  
    idfstore = {}
    wordCount = {}
    num = len(morListGroup)

    for i in range(num):
        for word in morListGroup[i]:
            for j in range(0, ITWORDS): 
                if (itWordsList[j] == word): # IT用語かどうかの判定
                    allCount[i] = wordCount.setdefault(word, 0)
                    wordCount[word]+=1
                    it_words_key_list.append(word)
        allCount[i] = wordCount
        wordCount = {}          # 各説明文章ごとに形態素出現回数を格納

    #print(convertJapanese(allCount))

    for i in range(num):
        for word in morListGroup[i]:
           wordCount.setdefault(word, 0) 
        for word in allCount[i]:
            wordCount[word] += 1
        sub_idf = wordCount     # ある単語の文章あたりの出現回数を辞書に格納

    #print '------------------------------------'
    #print(convertJapanese(sub_idf))

    for i in range(num):
        for word in allCount[i]:
            #for j in range(0, ITWORDS): 
                #if (itWordsList[j] == word): # IT用語かどうかの判定
                    #idfstore[itWordsList[j]] = math.log(1.0 * math.fabs(num) / math.fabs(sub_idf[itWordsList[j]]))    # fabsは絶対値
            idfstore[word] = math.log(1.0 * math.fabs(num) / math.fabs(sub_idf[word]))    # fabsは絶対値
                    #print idfstore[word]
            it_words_dic[word] = idfstore[word] 


## 文書のIDFを求めるメソッド ##
def calc_doc_idf(file):
    sum = 0
    for line in open(file, 'r'):
        for j in range(0, ITWORDS): 
            if (itWordsList[j] in line): # 文書のなかに含まれるIT用語を取り出す
                if (itWordsList[j] in it_words_key_list):
                    value = it_words_dic[itWordsList[j]]
                    #print file, (convertJapanese(itWordsList[j])), value
                    sum += value
        print file, '\t\t', sum
        sum = 0

# IDFの辞書をIDFの降順で並べて出力
def sort_idf():
    for word, count in sorted(it_words_dic.items(),key = lambda x:x[1],reverse = True):
        #print(convertJapanese(it_words_dic))
        #print(convertJapanese(it_words_dic.items()))
        print '%-16s %2.3f' % (word,count)

##### メソッド定義（終了）#####


# 空のリストを生成
itWordsList = [] # IT用語のリスト
ITWORDS = 9175 # 確認するIT用語の数を指定
morListGroup = [] # 全テキストの形態素
idfITwordsList = [] # IDF計算で対象となるIT用語
it_words_dic = {} # IDFの辞書
it_words_key_list = []

# IT用語が入ったテキストを開いて読み込む
makeWordList()

# IT用語が入っているかどうか確認
for file in glob.glob('e-words_430/*.txt'):
    #print file
    counter, morNum = checkITWords(file)
    #print morNum, counter, float(counter)/morNum
    #print float(counter)/morNum

#print(convertJapanese(itWordsList))

calc_idf(morListGroup)
sort_idf()
#print(convertJapanese(it_words_dic))

#for file in glob.glob('e-words_430/*.txt'):
    #calc_doc_idf(file)
