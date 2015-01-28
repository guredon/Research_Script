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


## 形態素解析を行うメソッド ##
def MorphologicalAnalysis(file):

    morList = []    # 形態素解析結果のリスト

    for line in open(file, 'r'):
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
    morListGroup.append(morList)
    #return morList

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


## IT用語をKey, IDFをValueとした辞書を作成するメソッド ##
def make_idf_dic(morListGroup):
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
            it_words_idf_dic[word] = idfstore[word] 


## 文書のIDFを求めるメソッド ##
def calc_doc_idf(file):
    sum = 0
    for line in open(file, 'r'):
        for j in range(0, ITWORDS): 
            if (itWordsList[j] in line): # 文書のなかに含まれるIT用語を取り出す
                if (itWordsList[j] in it_words_key_list): # IT用語と判断された形態素であるか
                    value = it_words_idf_dic[itWordsList[j]]
                    #print file, (convertJapanese(itWordsList[j])), value
                    sum += value
        print file, '\t\t\t', sum
        #tail = file.split('/')
        file_decode = file.decode('utf-8')
        it_doc_idf_dic[file_decode] = sum
        sum = 0

# IDFの辞書をIDFの降順で並べて出力
def sort_idf(dic):
    for word, count in sorted(dic.items(), key = lambda x:x[1], reverse = True):
        #print(convertJapanese(it_words_idf_dic))
        #print(convertJapanese(it_words_idf_dic.items()))
        print '%-50s %2.3f' % (word,count)

##### メソッド定義（終了）#####


# 空のリストを生成

ITWORDS = 9175 # 確認するIT用語の数を指定
itWordsList = [] # IT用語一覧
morListGroup = [] # 全テキストの形態素
idfITwordsList = [] # IDF計算で対象となるIT用語
it_words_key_list = [] # IT用語と判断された形態素のリスト
it_words_idf_dic = {} # IT用語をKey, IDFをValueとした辞書
it_doc_idf_dic = {} # IT用語を説明した文書名をKey, IDFをValueとした辞書

# IT用語が入ったテキストを開いて読み込む
makeWordList()

# 形態素解析を行う
for file in glob.glob('IT_700_430/*'):
    MorphologicalAnalysis(file)

# 辞書を作成する
make_idf_dic(morListGroup)

# 文書のIDFを求める
for file in glob.glob('e-words_430/*'):
    calc_doc_idf(file)

# IDFを降順にソートする
#sort_idf(it_doc_idf_dic)
