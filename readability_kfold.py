import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import svm
from sklearn import metrics

# カタカナの割合
fp = open("difficult_j.txt","rb");
rateWords_list  = np.fromfile(fp, dtype = np.float, sep = '\n');
fp.close();
a1 = rateWords_list.reshape((rateWords_list.size, 1))
#print a1

fp = open("easy_j.txt","rb");
rate700_list  = np.fromfile(fp, dtype = np.float, sep = '\n');
fp.close();
a2 = rate700_list.reshape((rate700_list.size, 1))
#print a2

a = np.r_[a1, a2]
#print a


# 難易度のラベル
b1 = np.ones(a1.size)
b2 = np.zeros(a2.size)

b = np.r_[b1, b2]
#print b

# K-Foldを使う（3分割）
scores = cross_validation.KFold(a.size, n_folds=3, shuffle=True)

# 学習データとテストデータに分割
for train_index, test_index in scores:
    print("TRAIN:", train_index, "TEST:", test_index)
    a_train, a_test = a[train_index], a[test_index]
    b_train, b_test = b[train_index], b[test_index]

# 正解ラベル
print b_test

# 分類器はSVMを使う
classifier = svm.SVC(C=1.0, kernel='linear')

# 学習
fitted = classifier.fit(a_train, b_train)

# 予測
predicted = fitted.predict(a_test)
print predicted

# 正解率
print metrics.accuracy_score(predicted, b_test)
