import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import svm
from sklearn import metrics
import csv
import sys
import codecs
import re
import pprint 


## 日本語を扱うメソッド ##
def convertJapanese(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)


## ベクトル作成（前半のラベルが易しい, 後半のラベルが難しい）
def make_vector():

    easy_list = []
    difficult_list = []

    f = open('reverse_chara_score_easy3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            easy_list.extend([round(float(row[6]), 3), round(float(row[7]), 3)])
        #print easy_list
        p = np.array(easy_list)
        a1 = p.reshape((RESHAPE_ROW, 2))
        #print a1
    finally:
        f.close()
    
    f = open('reverse_chara_score_difficult3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            #difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            difficult_list.extend([round(float(row[6]), 3), round(float(row[7]), 3)])
        q = np.array(difficult_list)
        a2 = q.reshape((RESHAPE_ROW, 2))
        #print a2
    finally:
        f.close()

    a = np.r_[a1, a2]

    b1 = np.zeros(RESHAPE_ROW)
    b2 = np.ones(RESHAPE_ROW)
    b = np.r_[b1, b2]

    return a, b


## ベクトル作成（ラベルをつける順番が複雑）
def make_vector_complex():

    easy_list = []
    difficult_list = []

    f = open('reverse_chara_score_easy3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            easy_list.extend([round(float(row[6]), 3), round(float(row[7]), 3)])
        #print easy_list
        p = np.array(easy_list)
        a1 = p.reshape((RESHAPE_ROW, 2))
        #print a1
    finally:
        f.close()
    
    f = open('reverse_chara_score_difficult3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            #difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            difficult_list.extend([round(float(row[6]), 3), round(float(row[7]), 3)])
        q = np.array(difficult_list)
        a2 = q.reshape((RESHAPE_ROW, 2))
        #print a2
    finally:
        f.close()

    easy_list = []
    difficult_list = []
    
    
    f = open('reverse_chara_score_difficult.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[7]), 3)])
        #print easy_list
        s = np.array(easy_list)
        a3 = s.reshape((REVERSE_RESHAPE_ROW, 6))
    finally:
        f.close()
    
    
    f = open('reverse_chara_score_easy.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # 最初の1行を取り出す
        for row in reader:
            difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
            #difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[7]), 3)])
        #print easy_list
        t = np.array(difficult_list)
        a4 = t.reshape((REVERSE_RESHAPE_ROW, 6))
    finally:
        f.close()


    a = np.r_[a1, a2, a3, a4]

    b1 = np.zeros(RESHAPE_ROW)
    b2 = np.ones(RESHAPE_ROW)
    b3 = np.zeros(REVERSE_RESHAPE_ROW)
    b4 = np.ones(REVERSE_RESHAPE_ROW)
    b = np.r_[b1, b2]

    return a, b


if __name__ == '__main__':

    RESHAPE_ROW = 10
    REVERSE_RESHAPE_ROW = 10
    DIVISION = 3
    
    a, b = make_vector()
    #a, b = make_vector_complex()
    
    # K-Foldを使う（3分割）
    scores = cross_validation.KFold(RESHAPE_ROW * 2, n_folds=DIVISION, shuffle=True)
    
    sum_precision = 0     # 分類精度の合計値
    
    # 学習データとテストデータに分割
    for train_index, test_index in scores:
        print("TRAIN:", train_index, "TEST:", test_index)
        a_train, a_test = a[train_index], a[test_index]
        b_train, b_test = b[train_index], b[test_index]
        #print a_train
        #print a_test
        #print b_train
        print b_test
        print "------------------------------------------"
    
        # 正解ラベル
        #print b_test
        
        # 分類器はSVMを使う

        classifier = svm.SVC(C=1.0, kernel='linear')
        
        # 学習
        fitted = classifier.fit(a_train, b_train)
        
        # 予測
        predicted = fitted.predict(a_test)
        print predicted
        
        # 正解率
        print metrics.accuracy_score(predicted, b_test)
        
        sum_precision += metrics.accuracy_score(predicted, b_test)
    
    print sum_precision / DIVISION      # 分類精度
