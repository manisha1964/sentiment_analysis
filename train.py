#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import numpy as np
import csv, json, sys
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score, make_scorer
from sklearn.cross_validation import train_test_split
from scipy import sparse
from scipy.sparse import csr_matrix,csc_matrix
import pandas as pd

def load_fv(s):
    fv=[]
    #inp=open('%s/allfv.csv' % s, 'rb')
    cnt=1
    reader=pd.read_csv('%s/allfv.csv' % s, header=None, iterator=True)
	#print len(chunks)
    cnt=0
	
	#reader=pd.read_csv('%s/allfv.csv' % s, header=None, iterator=True)
    while(cnt<49987):
		cnt+=1
		ch=reader.get_chunk(1)
		#print ch
		row=[]
		for item in ch:
			#print item
			try:
				row.append(float(item))
			except:
				print cnt
				val=item.split('.')
				v=[]
				v.append(val[0])
				v.append(val[1])
				v='.'.join(v)
				v=float(v)
				#print item, v
				row.append(v)
		fv.append(row)
	
    print len(fv), len(fv[0])
    #, quoting=csv.QUOTE_NONNUMERIC
    # y = csv.reader(inp)
    # cnt=1
    # for row in y:
    # 	print cnt
    # 	cnt+=1
    # 	fv.append(row)

    print 'fv', len(fv)
    return fv

def load_label(s):
    lab=[]
    with open('%s/labels.txt' % s, 'rb') as lab:
        lab = json.load(lab)
    print 'labels', len(lab)
    return lab

def calc_pred(predicts, y_test):
    actual0pred0=0
    actual1pred0=0
    actual1pred1=0
    actual0pred1=0
    for i in range(len(predicts)):
        if predicts[i] == 0 and y_test[i] == 0:
            actual0pred0+=1
        elif predicts[i] == 0 and y_test[i] == 1:
            actual1pred0+=1
        elif predicts[i] == 1 and y_test[i] == 0:
            actual0pred1+=1
        elif predicts[i] == 1 and y_test[i] == 1:
            actual1pred1+=1
    print 'actual1pred1 = %d, actual0pred1 = %d, actual1pred0 = %d, actual0pred0 = %d\n' % (actual1pred1, actual0pred1, actual1pred0, actual0pred0)

def calc_exact_pred(exact_pred, predicts, y_test_arr):
    for val in range(len(exact_pred)):
        print (exact_pred[val], predicts[val], y_test_arr[val])

def count_pred(predicts, y_test_arr):
    cnt0=0
    cnt1=0
    cnt2=0
    for item in predicts:
        #print item, type(item)
        if item == -1.0:
            cnt0+=1
        if item == 0.0:
            cnt1+=1
        if item == 1.0:
            cnt2+=1
    print cnt0, cnt1, cnt2
            
#print 'load test'
#fvec_test=load_fv("test")

print 'load train'
fvec_train=load_fv("train")
print len(fvec_train)
# fv2=[]
# cnt=1
# for row in fvec_t:
# 	r2=[]
# 	print cnt
# 	cnt+=1
# 	for item in row:
# 		r2.append(float(item))
# 	fv2.append(r2)
# fvec_test=fv2
print len(fvec_train), type(fvec_train)
print 'loaded train'
lab_train=load_label("train")
#with open('test/labels.txt', 'rb') as ip:
#	lab_test=ip.readlines()
#print len(lab_test)
# l=[]
# for item in lab_test:
# 	item=item.rstrip('\n')
# 	#print item
# 	if item == 'negative':
# 		l.append(-1.0)
# 	elif item == 'positive':
# 		l.append(1.0)
# 	elif item == 'neutral':
# 		l.append(0.0)
# lab_test=l

#print type(fvec_test)
#print 'convert test to sparse'
#_test_arr = csr_matrix(fvec_test)
#print X_test_arr.data.nbytes
#sparse.save_npz("test/testmatrix.npz", X_test_arr)
#X_test_arr = sparse.load_npz("test/testmatrix.npz")
#print 'converted'

print 'convert train to sparse'
X_train_arr = csr_matrix(fvec_train)
print X_train_arr.data.nbytes
sparse.save_npz("train/trainmatrix.npz", X_train_arr)
#X_train_arr = sparse.load_npz("train/trainmatrix.npz") #load saved sparse matrix
print 'converted'
'''
#train_valid_test split
fvec_train, fvec_tes, lab_train, lab_te = train_test_split(X_train_arr, lab_train, test_size=0.0, random_state=1)
fvec_test, o, lab_test, o = train_test_split(X_test_arr, lab_test, test_size=0.0, random_state=1)



#convert to np arrays
X_train_arr=np.array(fvec_train).astype(float)
X_test_arr=np.array(fvec_test).astype(float)
y_train_arr = np.array(lab_train).astype(float)
y_test_arr = np.array(lab_test).astype(float)

#scoring={'recall': make_scorer(recall_score)}
k = [0.09, 0.1, 0.15, 0.2, 1, 10]
acc=0.0
for iter in k:
    clf=LogisticRegression(C=iter)
    score=(cross_val_score(clf, X_train_arr, y_train_arr, cv=5))
    print score
    score=score.mean()
    print score, iter
    if score > acc:
        acc=score
        maxiter=iter

clf=LogisticRegression(C=maxiter)
clf.fit(X_train_arr, y_train_arr)
predicts = clf.predict(X_test_arr)
#exact_pred = clf.predict_proba(X_test_arr)
#calc_exact_pred(exact_pred, predicts, y_test_arr)
#calc_pred(predicts, y_test_arr)
count_pred(predicts, y_test_arr)
print 'test accuracy'
print accuracy_score(predicts, y_test_arr), maxiter
print recall_score(y_test_arr, predicts, average='macro'), 'macro'
print recall_score(y_test_arr, predicts, average='micro'), 'micro'
print recall_score(y_test_arr, predicts, average='weighted'), 'weighted'
'''
#0.583279062195 1
#0.575708238359 0.2
