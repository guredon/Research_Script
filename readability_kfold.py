import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import svm
from sklearn import metrics
import csv
import sys

easy_list = []
difficult_list = []
RESHAPE_ROW = 40
REVERSE_RESHAPE_ROW = 10
DIVISION = 3

f = open('40_chara_score_easy.csv', 'rt')
try:
    reader = csv.reader(f)
    fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
    for row in reader:
        #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
        easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4])])
    #print easy_list
    p = np.array(easy_list)
    a1 = p.reshape((RESHAPE_ROW, 4))
    #print a1
finally:
    f.close()


f = open('40_chara_score_difficult.csv', 'rt')
try:
    reader = csv.reader(f)
    fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
    for row in reader:
        #difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
        difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4])])
    q = np.array(difficult_list)
    a2 = q.reshape((RESHAPE_ROW, 4))
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
        #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
        easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4])])
    #print easy_list
    s = np.array(easy_list)
    a3 = s.reshape((REVERSE_RESHAPE_ROW, 4))
    #print a1
finally:
    f.close()


f = open('reverse_chara_score_easy.csv', 'rt')
try:
    reader = csv.reader(f)
    fieldnames = next(reader) # $B:G=i$N(B1$B9T$r<h$j=P$9(B
    for row in reader:
        #easy_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4]), round(float(row[6]), 3), round(float(row[7]), 3)])
        difficult_list.extend([float(row[1]), float(row[2]), float(row[3]), float(row[4])])
    #print easy_list
    t = np.array(difficult_list)
    a4 = t.reshape((REVERSE_RESHAPE_ROW, 4))
    #print a1
finally:
    f.close()

## $B%+%?%+%J$N3d9g(B
#fp = open("difficult_j.txt", "rb");
#rateWords_list  = np.fromfile(fp, dtype = np.float, sep = '\n');
##print rateWords_list
#fp.close();
#a1 = rateWords_list.reshape((rateWords_list.size, 1))
##print a1
#
#fp = open("easy_j.txt", "rb");
#rate700_list  = np.fromfile(fp, dtype = np.float, sep = '\n');
#fp.close();
#a2 = rate700_list.reshape((rate700_list.size, 1))
##print a2

a = np.r_[a1, a2, a3, a4]
#print a

# $BFq0WEY$N%i%Y%k(B
#b1 = np.ones(a1.size)
#b2 = np.zeros(a2.size)
b1 = np.zeros(RESHAPE_ROW)
b2 = np.ones(RESHAPE_ROW)
b3 = np.zeros(REVERSE_RESHAPE_ROW)
b4 = np.ones(REVERSE_RESHAPE_ROW)

b = np.r_[b1, b2, b3, b4]
#print b


# K-Fold$B$r;H$&!J(B3$BJ,3d!K(B
scores = cross_validation.KFold(RESHAPE_ROW * 2, n_folds=DIVISION, shuffle=True)

sum = 0

# $B3X=,%G!<%?$H%F%9%H%G!<%?$KJ,3d(B
for train_index, test_index in scores:
    #print("TRAIN:", train_index, "TEST:", test_index)
    a_train, a_test = a[train_index], a[test_index]
    b_train, b_test = b[train_index], b[test_index]
    #print a_train
    #print a_test
    #print b_train
    #print b_test
    #print "------------------------------------------"


    # $B@52r%i%Y%k(B
    #print b_test
    
    # $BJ,N`4o$O(BSVM$B$r;H$&(B
    classifier = svm.SVC(C=1.0, kernel='linear')
    
    # $B3X=,(B
    fitted = classifier.fit(a_train, b_train)
    
    # $BM=B,(B
    predicted = fitted.predict(a_test)
    #print predicted
    
    # $B@52rN((B
    #print metrics.accuracy_score(predicted, b_test)
    
    sum += metrics.accuracy_score(predicted, b_test)

print sum / DIVISION

