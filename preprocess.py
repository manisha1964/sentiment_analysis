#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import preprocessing as p
import heuristics as h
import csv, sys, nltk

with open('test/testdataset.csv', 'rb') as inp:
    all=[]
    reader=csv.reader(inp)
    cnt=0
    for row in reader:
        mod=[]
        mod.append(cnt)
        cnt+=1
        #mod.append(row[2])
        psen = p.processAll(row[1])
        for item in psen.split():
            if item.lower() in h.NEGATE:
                psen=psen.replace(item, '__NEG')
        mod.append(psen)
        all.append(mod)
print len(all)
#print all[:5]
with open('test/data.csv', 'wb') as op:
    writer=csv.writer(op, lineterminator='\n')
    writer.writerows(all)
#with open('data.csv', 'rb') as ip:
#    reader=csv.reader(ip)
#    for item in reader:
#        print item
        #sys.exit()
 


#uni = [ a if(a[0:2]=='__') else a.lower() for a in re.findall(r"\w+", text) ]
#bi  = nltk.bigrams(uni)
#tri = nltk.trigrams(uni)

