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


## $BF|K\8l$r07$&%a%=%C%I(B ##
def convertJapanese(obj):
  pp = pprint.PrettyPrinter(indent=4, width=160)
  str = pp.pformat(obj)
  return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)


## $B%Y%/%H%k:n@.!JA0H>$N%i%Y%k$,0W$7$$(B, $B8eH>$N%i%Y%k$,Fq$7$$!K(B
def make_vector():

    easy_list = []
    difficult_list = []

    f = open('reverse_chara_score_easy3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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


## $B%Y%/%H%k:n@.!J%i%Y%k$r$D$1$k=gHV$,J#;(!K(B
def make_vector_complex():

    easy_list = []
    difficult_list = []

    f = open('reverse_chara_score_easy3.csv', 'rt')
    try:
        reader = csv.reader(f)
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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
        fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
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
    
    # K-Fold$B$r;H$&!J(B3$BJ,3d!K(B
    scores = cross_validation.KFold(RESHAPE_ROW * 2, n_folds=DIVISION, shuffle=True)
    
    sum_precision = 0     # $BJ,N`@:EY$N9g7WCM(B
    
    # $B3X=,%G!<%?$H%F%9%H%G!<%?$KJ,3d(B
    for train_index, test_index in scores:
        print("TRAIN:", train_index, "TEST:", test_index)
        a_train, a_test = a[train_index], a[test_index]
        b_train, b_test = b[train_index], b[test_index]
        #print a_train
        #print a_test
        #print b_train
        print b_test
        print "------------------------------------------"
    
        # $B@52r%i%Y%k(B
        #print b_test
        
        # $BJ,N`4o$O(BSVM$B$r;H$&(B

        classifier = svm.SVC(C=1.0, kernel='linear')
        
        # $B3X=,(B
        fitted = classifier.fit(a_train, b_train)
        
        # $BM=B,(B
        predicted = fitted.predict(a_test)
        print predicted
        
        # $B@52rN((B
        print metrics.accuracy_score(predicted, b_test)
        
        sum_precision += metrics.accuracy_score(predicted, b_test)
    
    print sum_precision / DIVISION      # $BJ,N`@:EY(B
